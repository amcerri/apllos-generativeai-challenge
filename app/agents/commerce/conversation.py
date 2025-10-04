"""
Commerce conversation handler (document-aware Q&A).

Overview
--------
Handle follow-up questions about previously processed commerce documents using
LLM-powered analysis. Provides intelligent responses based on document context,
enabling natural conversations about orders, invoices, and other commercial
documents within the user session.

Design
------
- Input: user question and document context from CommerceContextManager
- Output: contextual answer with insights and analysis
- LLM-powered: uses OpenAI for intelligent document analysis
- Context-aware: leverages full document structure for accurate responses
- Business-focused: provides actionable insights and recommendations

Integration
-----------
- Used by commerce agent for follow-up questions
- Integrates with CommerceContextManager for document retrieval
- Returns Answer-compatible responses for consistent UI

Usage
-----
>>> from app.agents.commerce.conversation import CommerceConversationHandler
>>> handler = CommerceConversationHandler()
>>> response = handler.answer_question(
...     question="Qual é o valor total deste pedido?",
...     context={"document": {...}, "thread_id": "123"}
... )
>>> response["text"]
'O valor total do pedido PO-2024-001 é R$ 15.750,00...'
"""

from __future__ import annotations

import json
import os
from typing import Any

try:  # Optional logger
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)

# Import memory manager
try:
    from app.agents.commerce.memory import get_memory_manager
    _memory_available = True
except Exception:  # pragma: no cover - optional
    _memory_available = False
    get_memory_manager = None


# Tracing (optional; single alias)
start_span: Any
try:
    from app.infra.tracing import start_span as _start_span
    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span


# Optional OpenAI client
openai: Any = None
try:
    import openai as _openai
    openai = _openai
except Exception:  # pragma: no cover - optional
    pass


# Optional Answer contract
try:
    from app.contracts.answer import Answer
    _answer_available = True
except Exception:  # pragma: no cover - optional
    _answer_available = False
    Answer = None


__all__ = ["CommerceConversationHandler"]


# ---------------------------------------------------------------------------
# Commerce Conversation Handler
# ---------------------------------------------------------------------------
class CommerceConversationHandler:
    """Handle questions about commerce documents using LLM analysis."""

    def __init__(self) -> None:
        self.log = get_logger("agent.commerce.conversation")

    def answer_question(
        self,
        *,
        question: str,
        context: dict[str, Any] | None = None,
        thread_id: str | None = None
    ) -> dict[str, Any]:
        """
        Answer question about commerce documents using document context.

        Args:
            question: User's question about documents.
            context: Document context containing the processed document.
            thread_id: Optional thread ID for logging.

        Returns:
            Answer-compatible response with text, meta, and insights.

        Raises:
            ValueError: If question is empty or invalid.
            RuntimeError: If document context is invalid or missing.
        """
        with start_span("agent.commerce.conversation"):
            question = (question or "").strip()
            if not question:
                return self._error_response("Pergunta não fornecida")
            
            # Use document context directly (simplified approach)
            if context and "document" in context:
                document = context["document"]
                if document:
                    return self._answer_with_context(
                        question=question,
                        document=document,
                        context=context,
                        thread_id=thread_id
                    )
            
            # No context available
            return self._no_context_response(question)

    def _answer_with_memory(
        self,
        question: str,
        matching_orders: list,
        thread_id: str | None
    ) -> dict[str, Any]:
        """Answer question using memory search results."""
        
        # Check for OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or openai is None:
            return self._fallback_memory_response(question, matching_orders)
        
        try:
            return self._answer_with_llm_memory(
                question=question,
                matching_orders=matching_orders,
                api_key=api_key,
                thread_id=thread_id
            )
        except Exception as e:
            self.log.error("LLM memory conversation failed", error=str(e), thread_id=thread_id)
            return self._fallback_memory_response(question, matching_orders)

    def _answer_with_context(
        self,
        question: str,
        document: dict[str, Any],
        context: dict[str, Any],
        thread_id: str | None
    ) -> dict[str, Any]:
        """Answer question using document context (legacy method)."""
        
        # Check for OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or openai is None:
            return self._fallback_response(question, document)
        
        try:
            return self._answer_with_llm(
                question=question,
                document=document,
                context=context,
                api_key=api_key,
                thread_id=thread_id
            )
        except Exception as e:
            self.log.error("LLM conversation failed", error=str(e), thread_id=thread_id)
            return self._fallback_response(question, document)

    def _answer_with_llm_memory(
        self,
        question: str,
        matching_orders: list,
        api_key: str,
        thread_id: str | None
    ) -> dict[str, Any]:
        """Answer question using OpenAI LLM with memory search results."""
        
        # Build system prompt for memory-based answers
        system_prompt = self._build_memory_system_prompt()
        
        # Build user message with matching orders
        user_message = self._build_memory_user_message(question, matching_orders)
        
        # Create OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,
            max_tokens=1200,
        )
        
        # Parse response
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from OpenAI")
        
        # Build response
        result = {
            "text": content.strip(),
            "meta": {
                "question_type": self._classify_question(question),
                "orders_found": len(matching_orders),
                "model": "gpt-4o-mini",
                "tokens_used": response.usage.total_tokens if response.usage else None,
                "thread_id": thread_id,
                "memory_search": True
            },
            "artifacts": {
                "matching_orders": [
                    {
                        "order_id": order.order_id,
                        "doc_type": order.doc_type,
                        "customer_name": order.customer_name,
                        "total_value": order.total_value,
                        "currency": order.currency,
                        "items_count": len(order.items)
                    }
                    for order in matching_orders
                ],
                "question": question
            },
            "followups": self._suggest_memory_followups(question, matching_orders)
        }
        
        self.log.info(
            "Memory-based question answered successfully",
            thread_id=thread_id,
            orders_found=len(matching_orders),
            question_length=len(question),
            response_length=len(content),
            tokens_used=response.usage.total_tokens if response.usage else None
        )
        
        return self._coerce_answer(result)

    def _build_memory_system_prompt(self) -> str:
        """Build system prompt for memory-based commerce conversation."""
        return """Você é um assistente especializado em análise de documentos comerciais com acesso a múltiplos pedidos/ordens. Sua função é responder perguntas sobre pedidos específicos ou fazer análises comparativas entre diferentes documentos.

INSTRUÇÕES:
- Responda sempre em português brasileiro
- Use os dados exatos dos documentos fornecidos
- Seja preciso com valores, datas e quantidades
- Quando houver múltiplos pedidos, faça comparações quando relevante
- Se uma informação não estiver nos documentos, diga claramente
- Use formatação clara com valores monetários (R$ X,XX)
- Destaque informações importantes com emojis apropriados

TIPOS DE PERGUNTAS COMUNS:
- Busca específica: "ordem das canetas azuis", "pedido do João"
- Valores e totais: "Qual o valor total?", "Quanto custa o item X?"
- Itens e quantidades: "Quais são os itens?", "Quantos produtos tem?"
- Comparações: "Qual pedido é maior?", "Compare os valores"
- Análises: "Há algum problema?", "O que você recomenda?"

FORMATO DE RESPOSTA:
- Identifique claramente qual(is) pedido(s) está respondendo
- Resposta direta à pergunta
- Dados específicos dos documentos
- Insights ou observações relevantes (quando aplicável)
- Formatação clara e profissional"""

    def _build_memory_user_message(self, question: str, matching_orders: list) -> str:
        """Build user message with question and matching orders."""
        
        parts = []
        
        # Add question
        parts.append(f"PERGUNTA: {question}")
        parts.append("")
        
        # Add matching orders
        parts.append(f"=== PEDIDOS ENCONTRADOS ({len(matching_orders)}) ===")
        
        for i, order in enumerate(matching_orders, 1):
            parts.append(f"\n--- PEDIDO {i} ---")
            parts.append(f"ID: {order.order_id}")
            parts.append(f"Tipo: {order.doc_type}")
            if order.customer_name:
                parts.append(f"Cliente: {order.customer_name}")
            parts.append(f"Moeda: {order.currency}")
            if order.order_date:
                parts.append(f"Data: {order.order_date}")
            parts.append(f"Valor Total: R$ {order.total_value:.2f}")
            parts.append(f"Processado em: {order.processed_at.strftime('%Y-%m-%d %H:%M')}")
            
            # Add items (limit to first 5 for brevity)
            if order.items:
                parts.append("Itens:")
                for j, item in enumerate(order.items[:5]):
                    item_line = f"  {j+1}. "
                    if item.get("name"):
                        item_line += item["name"]
                    if item.get("qty") and item.get("unit_price"):
                        item_line += f" - {item['qty']}x R$ {item['unit_price']:.2f}"
                    if item.get("line_total"):
                        item_line += f" = R$ {item['line_total']:.2f}"
                    parts.append(item_line)
                
                if len(order.items) > 5:
                    parts.append(f"  ... e mais {len(order.items) - 5} itens")
            
            # Add risks if any
            risks = order.metadata.get("risks", [])
            if risks:
                parts.append("Alertas:")
                for risk in risks:
                    parts.append(f"  ⚠️ {risk}")
        
        return "\n".join(parts)

    def _suggest_memory_followups(self, question: str, matching_orders: list) -> list[str]:
        """Suggest relevant follow-up questions for memory-based answers."""
        followups = []
        
        if len(matching_orders) > 1:
            followups.extend([
                "Compare os valores dos pedidos",
                "Qual pedido tem mais itens?",
                "Há diferenças nos fornecedores?"
            ])
        else:
            order = matching_orders[0]
            followups.extend([
                f"Qual é o valor total do pedido {order.order_id}?",
                "Quais são os principais itens?",
                "Há algum problema neste pedido?"
            ])
        
        return followups[:3]

    def _fallback_memory_response(self, question: str, matching_orders: list) -> dict[str, Any]:
        """Provide fallback response when LLM is not available for memory search."""
        
        if not matching_orders:
            return self._no_context_response(question)
        
        text = f"🔍 Encontrei {len(matching_orders)} pedido(s) relacionado(s) à sua pergunta.\n\n"
        
        for i, order in enumerate(matching_orders, 1):
            text += f"**Pedido {i}:**\n"
            text += f"• ID: {order.order_id}\n"
            text += f"• Tipo: {order.doc_type}\n"
            if order.customer_name:
                text += f"• Cliente: {order.customer_name}\n"
            text += f"• Valor: R$ {order.total_value:.2f}\n"
            text += f"• Itens: {len(order.items)}\n\n"
        
        text += "⚠️ Sistema de análise temporariamente indisponível. "
        text += "Informações básicas mostradas acima."
        
        return self._coerce_answer({
            "text": text,
            "meta": {
                "orders_found": len(matching_orders),
                "fallback": True,
                "memory_search": True
            },
            "artifacts": {
                "matching_orders": [
                    {
                        "order_id": order.order_id,
                        "doc_type": order.doc_type,
                        "total_value": order.total_value
                    }
                    for order in matching_orders
                ]
            },
            "followups": ["Tente novamente em alguns instantes"]
        })

    def _no_context_response(self, question: str) -> dict[str, Any]:
        """Response when no context or memory is available."""
        return self._coerce_answer({
            "text": "❌ Não encontrei nenhum documento comercial processado para responder sua pergunta. "
                   "Por favor, envie um documento primeiro (PDF, DOCX ou TXT) para que eu possa analisá-lo.",
            "meta": {
                "no_context": True,
                "suggestion": "Envie um documento comercial primeiro"
            },
            "artifacts": {},
            "followups": [
                "Como enviar um documento?",
                "Que tipos de documentos são aceitos?",
                "Como funciona o processamento?"
            ]
        })

    def _answer_with_llm(
        self,
        question: str,
        document: dict[str, Any],
        context: dict[str, Any],
        api_key: str,
        thread_id: str | None
    ) -> dict[str, Any]:
        """Answer question using OpenAI LLM."""
        
        # Build system prompt
        system_prompt = self._build_system_prompt()
        
        # Build user message with document context
        user_message = self._build_user_message(question, document, context)
        
        # Create OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3,  # Slightly higher for more natural responses
            max_tokens=1000,
        )
        
        # Parse response
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from OpenAI")
        
        # Extract document info for metadata
        doc_info = document.get("doc", {})
        doc_type = doc_info.get("doc_type", "unknown")
        doc_id = doc_info.get("doc_id", "N/A")
        
        # Build response
        result = {
            "text": content.strip(),
            "meta": {
                "doc_type": doc_type,
                "doc_id": doc_id,
                "question_type": self._classify_question(question),
                "conversation_count": context.get("conversation_count", 0) + 1,
                "model": "gpt-4o-mini",
                "tokens_used": response.usage.total_tokens if response.usage else None,
                "thread_id": thread_id
            },
            "artifacts": {
                "document_summary": self._extract_document_summary(document),
                "question": question
            },
            "followups": self._suggest_followups(question, document)
        }
        
        self.log.info(
            "Question answered successfully",
            thread_id=thread_id,
            doc_type=doc_type,
            doc_id=doc_id,
            question_length=len(question),
            response_length=len(content),
            tokens_used=response.usage.total_tokens if response.usage else None
        )
        
        return self._coerce_answer(result)

    def _build_system_prompt(self) -> str:
        """Build system prompt for commerce conversation."""
        return """You are a specialized assistant for commercial document analysis. Your function is to answer questions about purchase orders, invoices, quotes, and other commercial documents accurately and helpfully.

INSTRUCTIONS:
- Always respond in Brazilian Portuguese
- Use exact data from the provided document
- Be precise with values, dates, and quantities
- Provide business insights when relevant
- If information is not in the document, say so clearly
- Use clear formatting with monetary values (R$ X,XX)
- Highlight important information with appropriate emojis

COMMON QUESTION TYPES:
- Values and totals: "What is the total value?", "How much does item X cost?"
- Items and quantities: "What are the items?", "How many products are there?"
- Dates and deadlines: "When does it expire?", "What is the delivery date?"
- Suppliers and customers: "Who is the supplier?", "Customer data?"
- Analysis: "Is there any problem?", "What do you recommend?"

RESPONSE FORMAT:
- Direct answer to the question
- Specific document data
- Relevant insights or observations (when applicable)
- Clear and professional formatting"""

    def _build_user_message(
        self,
        question: str,
        document: dict[str, Any],
        context: dict[str, Any]
    ) -> str:
        """Build user message with question and document context."""
        
        parts = []
        
        # Add question
        parts.append(f"PERGUNTA: {question}")
        parts.append("")
        
        # Add document summary
        doc_info = document.get("doc", {})
        parts.append("=== DOCUMENTO ===")
        parts.append(f"Tipo: {doc_info.get('doc_type', 'Desconhecido')}")
        if doc_info.get("doc_id"):
            parts.append(f"ID: {doc_info['doc_id']}")
        if doc_info.get("currency"):
            parts.append(f"Moeda: {doc_info['currency']}")
        parts.append("")
        
        # Add buyer/vendor info
        if document.get("buyer"):
            parts.append("=== COMPRADOR ===")
            buyer = document["buyer"]
            for key, value in buyer.items():
                if value:
                    parts.append(f"{key}: {value}")
            parts.append("")
        
        if document.get("vendor"):
            parts.append("=== FORNECEDOR ===")
            vendor = document["vendor"]
            for key, value in vendor.items():
                if value:
                    parts.append(f"{key}: {value}")
            parts.append("")
        
        # Add dates
        if document.get("dates"):
            parts.append("=== DATAS ===")
            dates = document["dates"]
            for key, value in dates.items():
                if value:
                    parts.append(f"{key}: {value}")
            parts.append("")
        
        # Add items (limit to first 10 for brevity)
        items = document.get("items", [])
        if items:
            parts.append("=== ITENS ===")
            for i, item in enumerate(items[:10]):
                item_line = f"{i+1}. "
                if item.get("name"):
                    item_line += item["name"]
                if item.get("qty") and item.get("unit_price"):
                    item_line += f" - {item['qty']}x R$ {item['unit_price']:.2f}"
                if item.get("line_total"):
                    item_line += f" = R$ {item['line_total']:.2f}"
                parts.append(item_line)
            
            if len(items) > 10:
                parts.append(f"... e mais {len(items) - 10} itens")
            parts.append("")
        
        # Add totals
        totals = document.get("totals", {})
        if totals:
            parts.append("=== TOTAIS ===")
            if totals.get("subtotal"):
                parts.append(f"Subtotal: R$ {totals['subtotal']:.2f}")
            if totals.get("freight"):
                parts.append(f"Frete: R$ {totals['freight']:.2f}")
            if totals.get("grand_total"):
                parts.append(f"Total Geral: R$ {totals['grand_total']:.2f}")
            parts.append("")
        
        # Add terms
        if document.get("terms"):
            parts.append("=== CONDIÇÕES ===")
            terms = document["terms"]
            for key, value in terms.items():
                if value:
                    parts.append(f"{key}: {value}")
            parts.append("")
        
        # Add risks if any
        risks = document.get("risks", [])
        if risks:
            parts.append("=== ALERTAS ===")
            for risk in risks:
                parts.append(f"⚠️ {risk}")
            parts.append("")
        
        return "\n".join(parts)

    def _classify_question(self, question: str) -> str:
        """Classify the type of question being asked."""
        q_lower = question.lower()
        
        if any(word in q_lower for word in ["valor", "preço", "custo", "total", "quanto"]):
            return "pricing"
        elif any(word in q_lower for word in ["item", "produto", "quantidade", "quais"]):
            return "items"
        elif any(word in q_lower for word in ["data", "prazo", "entrega", "vencimento", "quando"]):
            return "dates"
        elif any(word in q_lower for word in ["fornecedor", "cliente", "comprador", "vendedor", "quem"]):
            return "parties"
        elif any(word in q_lower for word in ["problema", "risco", "alerta", "erro", "análise"]):
            return "analysis"
        else:
            return "general"

    def _extract_document_summary(self, document: dict[str, Any]) -> dict[str, Any]:
        """Extract key document information for artifacts."""
        doc_info = document.get("doc", {})
        totals = document.get("totals", {})
        items = document.get("items", [])
        
        return {
            "doc_type": doc_info.get("doc_type"),
            "doc_id": doc_info.get("doc_id"),
            "currency": doc_info.get("currency"),
            "grand_total": totals.get("grand_total"),
            "items_count": len(items),
            "has_risks": len(document.get("risks", [])) > 0
        }

    def _suggest_followups(self, question: str, document: dict[str, Any]) -> list[str]:
        """Suggest relevant follow-up questions."""
        question_type = self._classify_question(question)
        doc_type = document.get("doc", {}).get("doc_type", "")
        
        followups = []
        
        if question_type == "pricing":
            followups.extend([
                "Quais são os itens mais caros?",
                "Há descontos aplicados?",
                "Como está dividido o valor total?"
            ])
        elif question_type == "items":
            followups.extend([
                "Qual é o valor total dos itens?",
                "Há itens em falta ou com problemas?",
                "Quais são as quantidades de cada item?"
            ])
        elif question_type == "dates":
            followups.extend([
                "Há algum prazo em risco?",
                "Quando foi emitido o documento?",
                "Quais são as condições de pagamento?"
            ])
        else:
            # General suggestions based on document type
            if doc_type == "purchase_order":
                followups.extend([
                    "Qual é o valor total do pedido?",
                    "Quando é a data de entrega?",
                    "Quais são os principais itens?"
                ])
            elif doc_type == "invoice":
                followups.extend([
                    "Qual é o valor da fatura?",
                    "Quando vence o pagamento?",
                    "Há impostos inclusos?"
                ])
            else:
                followups.extend([
                    "Qual é o valor total?",
                    "Quais são os itens inclusos?",
                    "Há algum problema no documento?"
                ])
        
        return followups[:3]  # Limit to 3 suggestions

    def _fallback_response(self, question: str, document: dict[str, Any]) -> dict[str, Any]:
        """Provide fallback response when LLM is not available."""
        doc_info = document.get("doc", {})
        doc_type = doc_info.get("doc_type", "documento")
        doc_id = doc_info.get("doc_id", "N/A")
        
        text = f"📄 Pergunta sobre {doc_type} {doc_id} recebida.\n\n"
        text += "⚠️ Sistema de análise temporariamente indisponível. "
        text += "Aqui estão as informações básicas do documento:\n\n"
        
        # Add basic document info
        totals = document.get("totals", {})
        if totals.get("grand_total"):
            text += f"💰 Valor total: R$ {totals['grand_total']:.2f}\n"
        
        items = document.get("items", [])
        if items:
            text += f"📦 Itens: {len(items)} produtos/serviços\n"
        
        dates = document.get("dates", {})
        if dates:
            text += f"📅 Datas importantes: {len(dates)} registradas\n"
        
        return self._coerce_answer({
            "text": text,
            "meta": {
                "doc_type": doc_type,
                "doc_id": doc_id,
                "fallback": True
            },
            "artifacts": {"document_summary": self._extract_document_summary(document)},
            "followups": ["Tente novamente em alguns instantes"]
        })

    def _error_response(self, error_message: str) -> dict[str, Any]:
        """Return error response."""
        return self._coerce_answer({
            "text": f"❌ Erro: {error_message}",
            "meta": {"error": True},
            "artifacts": {},
            "followups": []
        })

    def _coerce_answer(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Convert payload to Answer if available, else return dict."""
        if _answer_available and Answer is not None:
            try:
                return Answer(
                    text=payload.get("text", ""),
                    meta=payload.get("meta", {}),
                    artifacts=payload.get("artifacts", {}),
                    followups=payload.get("followups", []),
                    chunks=payload.get("chunks", [])
                ).__dict__
            except Exception:
                pass
        return payload
