# Troubleshooting Guide: Common Issues and Solutions

This document provides a comprehensive guide for troubleshooting common issues in the Apllos Assistant system, including diagnostic procedures, solutions, and preventive measures.

## Troubleshooting Overview

The Apllos Assistant troubleshooting guide covers:

- **Common Issues**: Frequently encountered problems and their solutions
- **Diagnostic Procedures**: Step-by-step diagnostic processes
- **Log Analysis**: How to analyze logs for troubleshooting
- **Performance Issues**: Identifying and resolving performance problems
- **Security Issues**: Security-related troubleshooting
- **Preventive Measures**: Best practices to avoid issues

## Common Issues and Solutions

### 1. Database Connection Issues

**Symptoms**:
- Database connection errors
- Timeout errors
- Connection pool exhaustion
- Slow database queries

**Diagnostic Steps**:
```bash
# Check database status
make db-status

# Check database logs
docker logs apllos-db

# Test database connection
make db-psql
```

**Solutions**:
```python
# Check database configuration
from app.infra.db import get_engine
engine = get_engine()

# Test connection
try:
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")

# Check connection pool
print(f"Pool size: {engine.pool.size()}")
print(f"Checked out: {engine.pool.checkedout()}")
print(f"Overflow: {engine.pool.overflow()}")
```

**Prevention**:
- Monitor connection pool usage
- Set appropriate pool sizes
- Use connection timeouts
- Implement connection health checks

### 2. LLM API Issues

**Symptoms**:
- OpenAI API errors
- Rate limiting errors
- Timeout errors
- Invalid response errors

**Diagnostic Steps**:
```bash
# Check OpenAI API key
echo $OPENAI_API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models

# Check API usage
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/usage
```

**Solutions**:
```python
# Check LLM client configuration
from app.infra.llm_client import get_llm_client
client = get_llm_client()

# Test LLM client
try:
    response = await client.chat_completion(
        messages=[{"role": "user", "content": "Hello"}],
        model="gpt-4o-mini"
    )
    print("LLM client working")
except Exception as e:
    print(f"LLM client error: {e}")

# Implement retry logic
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def robust_llm_call(messages, **kwargs):
    return await client.chat_completion(messages, **kwargs)
```

**Prevention**:
- Monitor API usage and limits
- Implement exponential backoff
- Use circuit breakers
- Cache responses when appropriate

### 3. Routing Issues

**Symptoms**:
- Incorrect agent routing
- Low routing confidence
- Routing loops
- Fallback overuse

**Diagnostic Steps**:
```bash
# Check routing configuration
cat app/config/agents.yaml

# Check allowlist
cat app/routing/allowlist.json

# Test routing
python scripts/eval_routing.py
```

**Solutions**:
```python
# Check router configuration
from app.routing.llm_classifier import LLMClassifier
from app.routing.supervisor import supervise

# Test router
router = LLMClassifier()
decision = await router.classify("test query", {})
print(f"Router decision: {decision}")

# Test supervisor
supervised_decision = await supervise(decision, {})
print(f"Supervised decision: {supervised_decision}")

# Check routing signals
print(f"Signals: {decision.signals}")
print(f"Confidence: {decision.confidence}")
print(f"Reason: {decision.reason}")
```

**Prevention**:
- Monitor routing accuracy
- Update routing examples
- Validate allowlist
- Test routing changes

### 4. Performance Issues

**Symptoms**:
- Slow response times
- High memory usage
- High CPU usage
- Timeout errors

**Diagnostic Steps**:
```bash
# Check system resources
docker stats

# Check application logs
docker logs apllos-app

# Check database performance
make db-psql
SELECT * FROM pg_stat_activity;
```

**Solutions**:
```python
# Monitor performance metrics
import psutil
import time

def check_system_resources():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    print(f"CPU: {cpu_percent}%")
    print(f"Memory: {memory.percent}%")
    print(f"Disk: {disk.percent}%")
    
    if cpu_percent > 80:
        print("WARNING: High CPU usage")
    if memory.percent > 80:
        print("WARNING: High memory usage")
    if disk.percent > 80:
        print("WARNING: High disk usage")

# Optimize database queries
from app.infra.db import get_engine
engine = get_engine()

# Check slow queries
with engine.connect() as conn:
    result = conn.execute("""
        SELECT query, mean_time, calls 
        FROM pg_stat_statements 
        ORDER BY mean_time DESC 
        LIMIT 10
    """)
    for row in result:
        print(f"Query: {row.query}, Time: {row.mean_time}, Calls: {row.calls}")
```

**Prevention**:
- Monitor system resources
- Optimize database queries
- Implement caching
- Use connection pooling
- Set appropriate timeouts

### 5. Security Issues

**Symptoms**:
- Security violations
- Unauthorized access
- Data breaches
- Audit failures

**Diagnostic Steps**:
```bash
# Check security logs
grep "SECURITY" logs/app.log

# Check access logs
grep "ACCESS" logs/app.log

# Check audit logs
grep "AUDIT" logs/app.log
```

**Solutions**:
```python
# Check security configuration
from app.config.settings import get_settings
settings = get_settings()

print(f"SQL approval required: {settings.require_sql_approval}")
print(f"Sanitize SQL: {settings.executor_sanitize_sql}")
print(f"Allowed origins: {settings.api_allowed_origins}")

# Implement security checks
def validate_input(query: str) -> bool:
    # Check for SQL injection
    dangerous_patterns = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]
    if any(pattern in query.upper() for pattern in dangerous_patterns):
        return False
    
    # Check for XSS
    if "<script>" in query.lower():
        return False
    
    return True

# Implement access control
def check_access(user_id: str, resource: str) -> bool:
    # Check user permissions
    user_permissions = get_user_permissions(user_id)
    return resource in user_permissions
```

**Prevention**:
- Implement input validation
- Use access control
- Monitor security events
- Regular security audits
- Update security policies

## Diagnostic Procedures

### 1. System Health Check

**Complete Health Check**:
```bash
#!/bin/bash
# health-check.sh

echo "=== Apllos Assistant Health Check ==="

# Check database
echo "Checking database..."
if curl -f http://localhost:8000/ok > /dev/null 2>&1; then
    echo "✓ Database: OK"
else
    echo "✗ Database: FAILED"
fi

# Check LLM API
echo "Checking LLM API..."
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✓ OpenAI API Key: Set"
else
    echo "✗ OpenAI API Key: Not set"
fi

# Check services
echo "Checking services..."
if docker ps | grep -q apllos-app; then
    echo "✓ App container: Running"
else
    echo "✗ App container: Not running"
fi

if docker ps | grep -q apllos-db; then
    echo "✓ Database container: Running"
else
    echo "✗ Database container: Not running"
fi

# Check logs
echo "Checking logs..."
if [ -f "logs/app.log" ]; then
    echo "✓ Log file: Exists"
    echo "Recent errors:"
    tail -n 20 logs/app.log | grep -i error
else
    echo "✗ Log file: Not found"
fi

echo "=== Health Check Complete ==="
```

### 2. Performance Analysis

**Performance Diagnostic**:
```python
import asyncio
import time
import psutil
from app.infra.metrics import get_metrics

class PerformanceDiagnostic:
    def __init__(self):
        self.metrics = get_metrics()
        self.start_time = time.time()
    
    async def run_diagnostic(self):
        print("=== Performance Diagnostic ===")
        
        # Check system resources
        await self.check_system_resources()
        
        # Check database performance
        await self.check_database_performance()
        
        # Check LLM performance
        await self.check_llm_performance()
        
        # Check application performance
        await self.check_application_performance()
        
        print("=== Diagnostic Complete ===")
    
    async def check_system_resources(self):
        print("\n--- System Resources ---")
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        print(f"CPU Usage: {cpu_percent}%")
        print(f"Memory Usage: {memory.percent}%")
        print(f"Disk Usage: {disk.percent}%")
        
        if cpu_percent > 80:
            print("WARNING: High CPU usage")
        if memory.percent > 80:
            print("WARNING: High memory usage")
        if disk.percent > 80:
            print("WARNING: High disk usage")
    
    async def check_database_performance(self):
        print("\n--- Database Performance ---")
        from app.infra.db import get_engine
        engine = get_engine()
        
        start_time = time.time()
        try:
            with engine.connect() as conn:
                result = conn.execute("SELECT 1")
                result.fetchone()
            duration = time.time() - start_time
            print(f"Database response time: {duration:.3f}s")
            
            if duration > 1.0:
                print("WARNING: Slow database response")
        except Exception as e:
            print(f"ERROR: Database connection failed: {e}")
    
    async def check_llm_performance(self):
        print("\n--- LLM Performance ---")
        from app.infra.llm_client import get_llm_client
        client = get_llm_client()
        
        start_time = time.time()
        try:
            response = await client.chat_completion(
                messages=[{"role": "user", "content": "Hello"}],
                model="gpt-4o-mini"
            )
            duration = time.time() - start_time
            print(f"LLM response time: {duration:.3f}s")
            
            if duration > 10.0:
                print("WARNING: Slow LLM response")
        except Exception as e:
            print(f"ERROR: LLM call failed: {e}")
    
    async def check_application_performance(self):
        print("\n--- Application Performance ---")
        # Check metrics
        print(f"Request count: {self.metrics.request_count.value()}")
        print(f"Error rate: {self.metrics.error_rate.value()}")
        print(f"Average response time: {self.metrics.response_time.value()}")

# Run diagnostic
async def main():
    diagnostic = PerformanceDiagnostic()
    await diagnostic.run_diagnostic()

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Log Analysis

**Log Analysis Script**:
```python
import re
from collections import Counter
from datetime import datetime, timedelta

class LogAnalyzer:
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.errors = []
        self.warnings = []
        self.info = []
    
    def analyze_logs(self):
        print("=== Log Analysis ===")
        
        # Read and parse logs
        self.parse_logs()
        
        # Analyze errors
        self.analyze_errors()
        
        # Analyze warnings
        self.analyze_warnings()
        
        # Analyze patterns
        self.analyze_patterns()
        
        print("=== Analysis Complete ===")
    
    def parse_logs(self):
        with open(self.log_file, 'r') as f:
            for line in f:
                if 'ERROR' in line:
                    self.errors.append(line.strip())
                elif 'WARNING' in line:
                    self.warnings.append(line.strip())
                elif 'INFO' in line:
                    self.info.append(line.strip())
    
    def analyze_errors(self):
        print(f"\n--- Error Analysis ---")
        print(f"Total errors: {len(self.errors)}")
        
        if self.errors:
            # Group errors by type
            error_types = Counter()
            for error in self.errors:
                if 'Database' in error:
                    error_types['Database'] += 1
                elif 'LLM' in error:
                    error_types['LLM'] += 1
                elif 'Routing' in error:
                    error_types['Routing'] += 1
                else:
                    error_types['Other'] += 1
            
            print("Error types:")
            for error_type, count in error_types.items():
                print(f"  {error_type}: {count}")
            
            # Show recent errors
            print("\nRecent errors:")
            for error in self.errors[-5:]:
                print(f"  {error}")
    
    def analyze_warnings(self):
        print(f"\n--- Warning Analysis ---")
        print(f"Total warnings: {len(self.warnings)}")
        
        if self.warnings:
            # Group warnings by type
            warning_types = Counter()
            for warning in self.warnings:
                if 'Performance' in warning:
                    warning_types['Performance'] += 1
                elif 'Security' in warning:
                    warning_types['Security'] += 1
                else:
                    warning_types['Other'] += 1
            
            print("Warning types:")
            for warning_type, count in warning_types.items():
                print(f"  {warning_type}: {count}")
    
    def analyze_patterns(self):
        print(f"\n--- Pattern Analysis ---")
        
        # Check for common patterns
        patterns = {
            'timeout': r'timeout',
            'connection': r'connection',
            'rate_limit': r'rate.limit',
            'memory': r'memory',
            'cpu': r'cpu'
        }
        
        for pattern_name, pattern in patterns.items():
            count = sum(1 for line in self.errors + self.warnings 
                       if re.search(pattern, line, re.IGNORECASE))
            if count > 0:
                print(f"  {pattern_name}: {count} occurrences")

# Run log analysis
analyzer = LogAnalyzer('logs/app.log')
analyzer.analyze_logs()
```

## Preventive Measures

### 1. Monitoring Setup

**Monitoring Configuration**:
```yaml
# monitoring.yml
monitoring:
  metrics:
    enabled: true
    interval: 30s
    endpoints:
      - /metrics
      - /health
      - /ready
  
  alerts:
    enabled: true
    rules:
      - name: "High Error Rate"
        condition: "error_rate > 0.1"
        duration: "5m"
        severity: "warning"
      
      - name: "High Response Time"
        condition: "response_time > 5s"
        duration: "5m"
        severity: "warning"
      
      - name: "High Memory Usage"
        condition: "memory_usage > 80%"
        duration: "5m"
        severity: "critical"
  
  dashboards:
    enabled: true
    refresh: "30s"
    panels:
      - title: "Request Rate"
        type: "graph"
        query: "rate(requests_total[5m])"
      
      - title: "Response Time"
        type: "graph"
        query: "histogram_quantile(0.95, request_duration_seconds)"
      
      - title: "Error Rate"
        type: "graph"
        query: "rate(requests_total{status=~\"5..\"}[5m])"
```

### 2. Health Checks

**Health Check Implementation**:
```python
from fastapi import FastAPI, HTTPException
from app.infra.db import get_engine
from app.infra.llm_client import get_llm_client

app = FastAPI()

@app.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "ok"}

@app.get("/ready")
async def readiness_check():
    """Readiness check"""
    try:
        # Check database
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        # Check LLM client
        client = get_llm_client()
        await client.health_check()
        
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Not ready: {str(e)}")

@app.get("/ok")
async def extended_health_check():
    """Extended health check"""
    health_status = {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    # Check database
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        health_status["services"]["database"] = "ok"
    except Exception as e:
        health_status["services"]["database"] = f"error: {str(e)}"
    
    # Check LLM client
    try:
        client = get_llm_client()
        await client.health_check()
        health_status["services"]["llm"] = "ok"
    except Exception as e:
        health_status["services"]["llm"] = f"error: {str(e)}"
    
    return health_status
```

### 3. Automated Recovery

**Recovery Scripts**:
```bash
#!/bin/bash
# recovery.sh

echo "=== Automated Recovery ==="

# Check if services are running
if ! docker ps | grep -q apllos-app; then
    echo "Starting app container..."
    docker-compose up -d app
fi

if ! docker ps | grep -q apllos-db; then
    echo "Starting database container..."
    docker-compose up -d db
fi

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Check health
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ Services recovered successfully"
else
    echo "✗ Services still not healthy"
    exit 1
fi

echo "=== Recovery Complete ==="
```

## Best Practices

### 1. Troubleshooting Best Practices
- **Document Issues**: Keep a record of common issues and solutions
- **Monitor Continuously**: Set up continuous monitoring
- **Test Regularly**: Regular testing of system components
- **Update Documentation**: Keep troubleshooting docs updated
- **Train Team**: Train team members on troubleshooting procedures

### 2. Prevention Best Practices
- **Proactive Monitoring**: Monitor before issues occur
- **Regular Maintenance**: Schedule regular maintenance
- **Update Dependencies**: Keep dependencies updated
- **Security Audits**: Regular security audits
- **Performance Testing**: Regular performance testing

### 3. Recovery Best Practices
- **Automated Recovery**: Implement automated recovery
- **Backup Strategies**: Implement comprehensive backup strategies
- **Disaster Recovery**: Plan for disaster recovery
- **Incident Response**: Have incident response procedures
- **Post-Incident Review**: Conduct post-incident reviews

This comprehensive troubleshooting guide should help developers identify and resolve issues in the Apllos Assistant system effectively.

---

**← [Back to Documentation Index](../README.md)**
