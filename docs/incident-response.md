# Incident Response: Application Failure Simulation

## Incident

**Incident Type:** Application Availability Failure
**Severity:** SEV-2 — Major Service Degradation / Unavailability
**Environment:** Flask Web Application
**Application:** AB Afric Infrastructure Asset Intelligence
**Status:** Resolved
**Incident Classification:** Simulated Incident

### Scenario

The AB Afric Asset Intelligence application becomes unavailable to users.

The incident response process follows this sequence:

```text
Application Failure
        ↓
Monitoring detects failure
        ↓
Alert triggered
        ↓
Engineer investigates
        ↓
Check service status
        ↓
Inspect logs
        ↓
Identify root cause
        ↓
Restore service
        ↓
Verify health endpoint
        ↓
Document incident
```

This simulation demonstrates the operational and troubleshooting approach an engineer would use when responding to an application availability incident.

---

## Detection

Monitoring detects that the application is no longer responding successfully to health checks.

The monitoring system reports repeated failed requests to the application's health endpoint.

Example:

```text
GET /health
HTTP 503 Service Unavailable
```

The failure threshold is exceeded and an alert is generated for the engineer responsible for the application.

### Detection signals

* Health endpoint returning unsuccessful responses
* Application requests failing
* Increased connection failures
* Users unable to access the application
* Application process potentially stopped or unhealthy

The objective at this stage is to confirm whether the issue is isolated to the monitoring system or represents a genuine application outage.

---

## Impact

The application is unavailable to users.

Potential business impact includes:

* Users cannot access the Asset Intelligence dashboard.
* Asset records cannot be viewed or updated.
* Maintenance information may be temporarily unavailable.
* Service request workflows may be interrupted.
* Operational decisions dependent on the application may be delayed.

### User impact

Users attempting to access the platform receive an error or are unable to establish a successful session.

### Data impact

No data loss is assumed in this simulation.

The incident concerns application availability rather than confirmed database corruption or data loss.

---

## Timeline

| Time  | Event                                                     |
| ----- | --------------------------------------------------------- |
| 10:00 | Monitoring detects failed application health checks.      |
| 10:01 | Availability alert is triggered.                          |
| 10:03 | Engineer acknowledges the incident.                       |
| 10:05 | Engineer checks application/service status.               |
| 10:08 | Application logs are inspected.                           |
| 10:12 | Root cause is identified.                                 |
| 10:15 | Application service is restarted/restored.                |
| 10:18 | Health endpoint is tested successfully.                   |
| 10:20 | Application availability is confirmed.                    |
| 10:30 | Incident is documented and preventive actions identified. |

> Times are simulated for demonstration purposes.

---

## Investigation

The engineer begins by confirming the scope of the failure.

### 1. Check service status

The application process and hosting service are checked to determine whether the application is running.

Example:

```bash
systemctl status ab-afric
```

If the application is running through a process manager, the corresponding process status is checked.

For example:

```bash
ps aux | grep python
```

The objective is to determine whether the application process has stopped, crashed, or become unresponsive.

### 2. Inspect application logs

Application logs are reviewed for errors immediately before the outage.

Example:

```bash
journalctl -u ab-afric --since "15 minutes ago"
```

Potential errors are investigated, including:

* Python exceptions
* Database connection failures
* Configuration errors
* Import errors
* Memory/resource exhaustion
* Failed application startup
* Dependency failures

### 3. Check database connectivity

Because the application depends on MySQL, database connectivity is also verified.

The engineer checks:

* MySQL service status
* Database connectivity
* Credentials/configuration
* Connection pool availability
* Recent database errors

### 4. Test the application locally

The application is tested from the server itself to determine whether the problem exists at the application layer or at the network/reverse-proxy layer.

Example:

```bash
curl http://127.0.0.1:5000/health
```

The response is compared with the externally observed failure.

### 5. Review recent changes

Recent deployments, configuration changes, dependency updates, or code changes are reviewed.

This helps establish whether the incident is related to a recent change.

---

## Root Cause

### Simulated Root Cause

The incident is caused by an application startup failure resulting from an invalid environment configuration.

The application attempts to start but fails during initialization because a required configuration value is missing or invalid.

Example:

```text
Application startup failed:
Required configuration variable is missing.
```

As a result:

1. The Flask application fails to initialize correctly.
2. The application service becomes unavailable.
3. Health checks fail.
4. Monitoring detects the failure.
5. An availability alert is generated.

### Root Cause Category

**Configuration / Deployment Failure**

This simulation demonstrates why application configuration should be validated before deployment.

---

## Resolution

The engineer restores the missing or invalid configuration value using the approved deployment configuration.

The configuration is validated before restarting the application.

The application service is then restarted.

Example:

```bash
sudo systemctl restart ab-afric
```

The service status is checked:

```bash
systemctl status ab-afric
```

The engineer confirms that the application process is running without startup errors.

---

## Verification

Service restoration is not considered complete until the application has been independently verified.

### 1. Check health endpoint

The engineer tests:

```bash
curl http://127.0.0.1:5000/health
```

Expected response:

```text
HTTP 200 OK
```

Example:

```json
{
  "status": "healthy"
}
```

### 2. Check application logs

Logs are reviewed again to confirm that no new startup or runtime errors are being generated.

### 3. Verify external access

The application is accessed through its normal URL to confirm that users can connect successfully.

### 4. Verify critical functionality

The engineer confirms that key application functions are operational, including:

* Login
* Dashboard
* Asset Register
* Maintenance workflows
* Service Requests
* Asset Intelligence

### 5. Confirm monitoring recovery

Monitoring must return to a healthy state and the availability alert must clear.

Only after these checks pass is the incident considered resolved.

---

## Preventive Actions

The incident highlights several improvements that should be implemented to reduce the probability and impact of similar failures.

### 1. Configuration validation

Validate required environment variables before application startup.

The application should fail with a clear configuration error rather than an ambiguous runtime failure.

### 2. Health checks

Maintain a dedicated health endpoint such as:

```text
/health
```

The endpoint should provide a simple indication of application availability.

### 3. Automated monitoring

Monitor:

* Application availability
* Health endpoint
* HTTP error rates
* Response latency
* Application process status
* Database connectivity

### 4. Alerting

Configure alerts for:

* Repeated health-check failures
* HTTP 5xx errors
* Application process crashes
* Database connection failures
* Resource exhaustion

### 5. Deployment validation

Before production deployment:

```text
Code change
    ↓
Automated tests
    ↓
Configuration validation
    ↓
Application startup test
    ↓
Health-check test
    ↓
Deployment
    ↓
Post-deployment verification
```

### 6. Logging

Ensure application logs contain sufficient information to identify:

* Startup failures
* Runtime exceptions
* Database failures
* Configuration problems
* Request failures

Logs should be centralized where possible and retained according to operational requirements.

### 7. Rollback strategy

Maintain a documented rollback procedure so that a failed deployment can be quickly reverted to the last known-good version.

### 8. Incident documentation

Every significant availability incident should produce a record containing:

* What happened
* When it happened
* Who detected it
* User impact
* Root cause
* Actions taken
* Recovery time
* Preventive actions

### 9. Post-incident review

After resolution, conduct a short post-incident review to identify:

* What worked well
* What slowed recovery
* What monitoring was missing
* What automation could prevent recurrence
* What operational documentation should be improved

---

## Engineering Lessons

This simulation demonstrates an incident-response mindset based on:

**Detect → Investigate → Diagnose → Restore → Verify → Learn**

The objective is not simply to restart an application.

A reliable engineer should:

1. Detect the failure quickly.
2. Establish the scope and impact.
3. Gather evidence before changing the system.
4. Identify the root cause.
5. Restore service safely.
6. Verify that the service is genuinely healthy.
7. Document the incident.
8. Implement preventive improvements.

This approach reduces mean time to recovery (MTTR) while improving system reliability and operational resilience.

---

## Incident Summary

| Category           | Result                                                                |
| ------------------ | --------------------------------------------------------------------- |
| Incident           | Application unavailable                                               |
| Detection          | Failed health checks                                                  |
| Impact             | Users unable to access application                                    |
| Investigation      | Service status, logs, database, recent changes                        |
| Root Cause         | Invalid application configuration                                     |
| Resolution         | Correct configuration and restart application                         |
| Verification       | Health endpoint and application functionality confirmed               |
| Preventive Actions | Monitoring, validation, testing, alerting, rollback and documentation |

---

**Note:** This is a simulated incident created as a portfolio demonstration of SRE incident-response methodology. It is not presented as a real production outage.
