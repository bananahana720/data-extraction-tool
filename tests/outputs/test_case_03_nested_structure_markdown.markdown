---
source: test_case_03_nested_structure.txt
format: text
---

ENTERPRISE SYSTEM CONFIGURATION MANIFEST
=========================================
Version: 3.2.1-alpha | Environment: PRODUCTION | Last Updated: 2024-10-28T09:23:47Z

# [SECTION 1: SERVICE TOPOLOGY]
-----------------------------

<system_architecture>
  <region id="us-east-1" priority="1">
    <availability_zone name="us-east-1a">
      <cluster type="kubernetes" version="1.28.3">
        <namespace name="production">
          <deployment name="api-gateway">
            <replicas>12</replicas>
            <resources>
              <requests>
                <cpu>2000m</cpu>
                <memory>4Gi</memory>
              </requests>
              <limits>
                <cpu>4000m</cpu>
                <memory>8Gi</memory>
              </limits>
            </resources>
            <containers>
              <container name="nginx-ingress" image="nginx:1.25.3-alpine">
                <ports>
                  <port containerPort="80" protocol="TCP"/>
                  <port containerPort="443" protocol="TCP"/>
                </ports>
                <env>
                  <variable name="UPSTREAM_SERVERS">api-service-1.prod.svc.cluster.local:8080,api-service-2.prod.svc.cluster.local:8080,api-service-3.prod.svc.cluster.local:8080</variable>
                  <variable name="RATE_LIMIT">1000</variable>
                  <variable name="TIMEOUT_SECONDS">30</variable>
                </env>
                <volumeMounts>
                  <mount name="ssl-certs" mountPath="/etc/nginx/ssl" readOnly="true"/>
                  <mount name="config" mountPath="/etc/nginx/conf.d" readOnly="true"/>
                </volumeMounts>
              </container>
            </containers>
            <service type="LoadBalancer">
              <selector>app=api-gateway</selector>
              <ports>
                <servicePort port="80" targetPort="80" protocol="TCP"/>
                <servicePort port="443" targetPort="443" protocol="TCP"/>
              </ports>
              <loadBalancerIP>203.0.113.47</loadBalancerIP>
            </service>
          </deployment>
          
          <deployment name="backend-services">
            <strategy type="RollingUpdate">
              <maxSurge>25%</maxSurge>
              <maxUnavailable>10%</maxUnavailable>
            </strategy>
            <template>
              <metadata>
                <labels>
                  <label key="app">backend-api</label>
                  <label key="tier">application</label>
                  <label key="version">v2.7.4</label>
                </labels>
                <annotations>
                  <annotation key="prometheus.io/scrape">true</annotation>
                  <annotation key="prometheus.io/port">9090</annotation>
                </annotations>
              </metadata>
            </template>
          </deployment>
        </namespace>
        
        <namespace name="data-layer">
          <statefulset name="postgres-cluster">
            <replicas>3</replicas>
            <serviceName>postgres-ha</serviceName>
            <podManagementPolicy>OrderedReady</podManagementPolicy>
            <volumeClaimTemplates>
              <template>
                <metadata>
                  <name>data</name>
                </metadata>
                <spec>
                  <accessModes>ReadWriteOnce</accessModes>
                  <storageClassName>fast-ssd</storageClassName>
                  <resources>
                    <requests>
                      <storage>500Gi</storage>
                    </requests>
                  </resources>
                </spec>
              </template>
            </volumeClaimTemplates>
          </statefulset>
        </namespace>
      </cluster>
    </availability_zone>
    
    <availability_zone name="us-east-1b">
      <!-- Replica configuration mirrors us-east-1a for HA -->
      <cluster type="kubernetes" version="1.28.3" role="failover">
        <replication_config>
          <mode>async</mode>
          <lag_threshold_seconds>5</lag_threshold_seconds>
        </replication_config>
      </cluster>
    </availability_zone>
  </region>
</system_architecture>

# [SECTION 2: APPLICATION CONFIGURATION]
--------------------------------------

{
  "application": {
    "name": "EnterprisePlatform",
    "version": "2.7.4",
    "build": {
      "number": 18473,
      "timestamp": "2024-10-27T22:14:33Z",
      "commit_sha": "a7f3d8c9e2b1f4a6c8d3e5f7a2b4c6d8e3f5a7b9",
      "branch": "release/v2.7.x"
    },
    "features": {
      "authentication": {
        "enabled": true,
        "providers": [
          {
            "type": "oauth2",
            "name": "google",
            "client_id": "${GOOGLE_CLIENT_ID}",
            "scopes": ["openid", "email", "profile"],
            "redirect_uri": "https://app.enterprise.com/auth/callback/google"
          },
          {
            "type": "saml",
            "name": "okta",
            "entity_id": "https://enterprise.okta.com",
            "sso_url": "https://enterprise.okta.com/app/saml/sso",
            "certificate": "${OKTA_CERT_BASE64}"
          },
          {
            "type": "ldap",
            "name": "active_directory",
            "server": {
              "host": "ldap.internal.corp",
              "port": 636,
              "use_ssl": true,
              "base_dn": "DC=corp,DC=internal",
              "bind_dn": "CN=ServiceAccount,OU=Apps,DC=corp,DC=internal",
              "bind_password": "${LDAP_BIND_PASSWORD}"
            },
            "user_filter": "(&(objectClass=person)(sAMAccountName={username}))",
            "group_filter": "(&(objectClass=group)(member={dn}))"
          }
        ],
        "session": {
          "timeout_minutes": 480,
          "refresh_enabled": true,
          "sliding_expiration": true,
          "cookie": {
            "name": "ENTERPRISE_SESSION",
            "secure": true,
            "http_only": true,
            "same_site": "Strict",
            "domain": ".enterprise.com"
          }
        },
        "mfa": {
          "enabled": true,
          "required_for_roles": ["admin", "finance", "engineering"],
          "methods": ["totp", "sms", "webauthn"],
          "grace_period_days": 7
        }
      },
      "api": {
        "rate_limiting": {
          "enabled": true,
          "strategies": [
            {
              "tier": "free",
              "requests_per_minute": 60,
              "requests_per_hour": 1000,
              "requests_per_day": 10000,
              "burst_allowance": 10
            },
            {
              "tier": "professional",
              "requests_per_minute": 300,
              "requests_per_hour": 10000,
              "requests_per_day": 100000,
              "burst_allowance": 50
            },
            {
              "tier": "enterprise",
              "requests_per_minute": 1000,
              "requests_per_hour": 50000,
              "requests_per_day": 1000000,
              "burst_allowance": 200
            }
          ],
          "bypass_ips": ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
        },
        "endpoints": {
          "/api/v2/users": {
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "auth_required": true,
            "roles": ["admin", "user_manager"],
            "cache": {
              "enabled": true,
              "ttl_seconds": 300,
              "vary_by": ["user_id", "organization_id"]
            }
          },
          "/api/v2/analytics": {
            "methods": ["GET", "POST"],
            "auth_required": true,
            "rate_limit_override": {
              "requests_per_minute": 30,
              "reason": "computationally_expensive"
            },
            "timeout_seconds": 60
          }
        }
      },
      "database": {
        "connections": {
          "primary": {
            "host": "postgres-master.internal.corp",
            "port": 5432,
            "database": "enterprise_prod",
            "username": "${DB_USERNAME}",
            "password": "${DB_PASSWORD}",
            "ssl_mode": "require",
            "pool": {
              "min_size": 10,
              "max_size": 100,
              "connection_timeout_seconds": 30,
              "idle_timeout_seconds": 600,
              "max_lifetime_seconds": 3600
            }
          },
          "replicas": [
            {
              "host": "postgres-replica-1.internal.corp",
              "port": 5432,
              "weight": 0.5,
              "role": "read_only"
            },
            {
              "host": "postgres-replica-2.internal.corp",
              "port": 5432,
              "weight": 0.5,
              "role": "read_only"
            }
          ],
          "analytics": {
            "host": "redshift-cluster.us-east-1.redshift.amazonaws.com",
            "port": 5439,
            "database": "analytics_warehouse",
            "username": "${REDSHIFT_USERNAME}",
            "password": "${REDSHIFT_PASSWORD}",
            "schema": "public"
          }
        },
        "migration": {
          "auto_apply": false,
          "location": "/db/migrations",
          "baseline_version": "1.0.0",
          "table": "schema_version"
        }
      },
      "cache": {
        "redis": {
          "mode": "cluster",
          "nodes": [
            {"host": "redis-1.cache.internal", "port": 6379},
            {"host": "redis-2.cache.internal", "port": 6379},
            {"host": "redis-3.cache.internal", "port": 6379},
            {"host": "redis-4.cache.internal", "port": 6379},
            {"host": "redis-5.cache.internal", "port": 6379},
            {"host": "redis-6.cache.internal", "port": 6379}
          ],
          "password": "${REDIS_PASSWORD}",
          "database": 0,
          "key_prefix": "enterprise:",
          "default_ttl_seconds": 3600,
          "strategies": {
            "session": {"ttl_seconds": 28800, "persist": true},
            "query_results": {"ttl_seconds": 300, "persist": false},
            "static_assets": {"ttl_seconds": 86400, "persist": true}
          }
        }
      },
      "messaging": {
        "kafka": {
          "bootstrap_servers": [
            "kafka-1.messaging.internal:9092",
            "kafka-2.messaging.internal:9092",
            "kafka-3.messaging.internal:9092"
          ],
          "topics": {
            "user_events": {
              "partitions": 12,
              "replication_factor": 3,
              "retention_hours": 168,
              "compression": "snappy"
            },
            "audit_logs": {
              "partitions": 24,
              "replication_factor": 3,
              "retention_hours": 2160,
              "compression": "lz4"
            },
            "transactions": {
              "partitions": 36,
              "replication_factor": 3,
              "retention_hours": 720,
              "compression": "zstd"
            }
          },
          "producer": {
            "acks": "all",
            "retries": 3,
            "batch_size_bytes": 16384,
            "linger_ms": 10,
            "buffer_memory_bytes": 33554432
          },
          "consumer": {
            "group_id": "enterprise-app-consumer",
            "auto_offset_reset": "earliest",
            "enable_auto_commit": false,
            "max_poll_records": 500
          }
        }
      },
      "observability": {
        "logging": {
          "level": "INFO",
          "format": "json",
          "outputs": [
            {
              "type": "stdout",
              "encoder": "json"
            },
            {
              "type": "file",
              "path": "/var/log/enterprise/app.log",
              "max_size_mb": 100,
              "max_backups": 10,
              "max_age_days": 30,
              "compress": true
            },
            {
              "type": "elasticsearch",
              "hosts": ["https://elasticsearch.logs.internal:9200"],
              "index": "enterprise-logs",
              "api_key": "${ELASTICSEARCH_API_KEY}"
            }
          ],
          "sampling": {
            "enabled": true,
            "rate": 0.1,
            "exclude_paths": ["/health", "/metrics"]
          }
        },
        "metrics": {
          "enabled": true,
          "port": 9090,
          "path": "/metrics",
          "namespace": "enterprise_app",
          "collectors": {
            "go": true,
            "process": true,
            "http": true,
            "database": true,
            "custom": true
          }
        },
        "tracing": {
          "enabled": true,
          "provider": "jaeger",
          "endpoint": "http://jaeger-collector.monitoring.internal:14268/api/traces",
          "sample_rate": 0.01,
          "always_sample_paths": ["/api/v2/critical/*"],
          "propagation_formats": ["w3c", "b3"]
        }
      }
    }
  }
}

# [SECTION 3: SECURITY POLICIES]
------------------------------

<security_configuration>
  <policies>
    <network_policy name="strict-egress">
      <rule id="1" action="ALLOW">
        <source>namespace:production</source>
        <destination>*.internal.corp</destination>
        <protocol>TCP</protocol>
        <ports>443,5432,6379,9092</ports>
      </rule>
      <rule id="2" action="DENY">
        <source>namespace:production</source>
        <destination>0.0.0.0/0</destination>
        <protocol>ANY</protocol>
        <exception>AWS API endpoints</exception>
      </rule>
    </network_policy>
    
    <rbac_policy name="role-based-access">
      <roles>
        <role name="admin" inherits="user,developer">
          <permissions>
            <permission resource="*" action="*" effect="allow"/>
          </permissions>
        </role>
        <role name="developer">
          <permissions>
            <permission resource="deployments" action="read,create,update" effect="allow"/>
            <permission resource="logs" action="read" effect="allow"/>
            <permission resource="secrets" action="read" effect="deny"/>
          </permissions>
        </role>
        <role name="user">
          <permissions>
            <permission resource="api:read" action="execute" effect="allow"/>
            <permission resource="api:write" action="execute" effect="conditional">
              <condition>user.verified == true AND user.mfa_enabled == true</condition>
            </permission>
          </permissions>
        </role>
      </roles>
    </rbac_policy>
  </policies>
</security_configuration>

[END OF CONFIGURATION MANIFEST]
Checksum: SHA256:8f4a7c3b2e9d1f6a8c5e3d7f2a9b4c6d8e3f5a7b9c1d4e6f8a2c5d7e9f3a6c8