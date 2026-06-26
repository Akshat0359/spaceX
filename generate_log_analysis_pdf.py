#!/usr/bin/env python3
"""Generate a professional PDF presentation for AI-Driven Log Analysis Platform."""

from fpdf import FPDF

class PresentationPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'AI-Driven Log Analysis and Diagnostics Platform', align='R')
        self.ln(5)
        self.set_draw_color(20, 120, 200)
        self.set_line_width(0.5)
        self.line(10, 13, 200, 13)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(20, 100, 180)
        self.ln(6)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(20, 100, 180)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(50, 50, 50)
        self.ln(4)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub_sub_title(self, title):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(80, 80, 80)
        self.ln(3)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text, indent=10):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.set_x(self.l_margin + indent)
        self.multi_cell(self.w - self.l_margin - self.r_margin - indent, 5.5, '- ' + text)
        self.ln(1)

    def bold_bullet(self, bold_part, normal_part, indent=10):
        self.set_x(self.l_margin + indent)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.write(5.5, '- ')
        self.set_font('Helvetica', 'B', 10)
        self.write(5.5, bold_part)
        self.set_font('Helvetica', '', 10)
        self.write(5.5, normal_part)
        self.ln(7)

    def code_block(self, text):
        self.set_font('Courier', '', 9)
        self.set_fill_color(235, 240, 250)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5, text, fill=True)
        self.ln(3)

    def table_row(self, cols, widths, bold=False, header=False):
        if header:
            self.set_font('Helvetica', 'B', 9)
            self.set_fill_color(20, 100, 180)
            self.set_text_color(255, 255, 255)
        elif bold:
            self.set_font('Helvetica', 'B', 9)
            self.set_fill_color(240, 245, 255)
            self.set_text_color(30, 30, 30)
        else:
            self.set_font('Helvetica', '', 9)
            self.set_fill_color(248, 250, 255)
            self.set_text_color(30, 30, 30)
        for i, (col, w) in enumerate(zip(cols, widths)):
            self.cell(w, 7, str(col), border=1, fill=True, align='C' if i > 0 else 'L')
        self.ln()


def generate():
    pdf = PresentationPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ═══════════════════════════════════════════
    # TITLE PAGE
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.ln(50)
    pdf.set_font('Helvetica', 'B', 26)
    pdf.set_text_color(20, 100, 180)
    pdf.cell(0, 15, 'AI-Driven Log Analysis', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, 'and Diagnostics Platform', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_draw_color(20, 100, 180)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, 'Scalable System Design for Distributed Infrastructure', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Processing ~1 TB of Log Data Daily', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(15)
    pdf.set_font('Helvetica', 'I', 11)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 8, 'System Design Presentation', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Yash Lohia', align='C', new_x="LMARGIN", new_y="NEXT")

    # ═══════════════════════════════════════════
    # 1. PROBLEM STATEMENT
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('1. Problem Statement')
    pdf.body_text(
        'Design a large-scale AI-driven log analysis and diagnostics system for a distributed '
        'infrastructure environment consisting of thousands of virtual machines, each generating '
        'approximately 1 GB of logs per day - resulting in nearly 1 TB of log data daily.'
    )
    pdf.sub_title('Log Sources')
    pdf.bullet('Console logs - stdout/stderr output from running applications')
    pdf.bullet('System logs - OS-level events (syslog, kernel logs, auth logs)')
    pdf.bullet('Application logs - Structured/unstructured output from application code')

    pdf.sub_title('Additional Data Sources')
    pdf.bullet('Application source code repositories')
    pdf.bullet('Historical incident and resolution data')
    pdf.bullet('Build and deployment metadata (optional)')

    pdf.sub_title('Core Challenge')
    pdf.body_text(
        'The system must automatically ingest, process, and analyze massive volumes of heterogeneous '
        'log data in real-time, detect anomalies and errors, correlate events across distributed systems, '
        'determine root causes, and recommend remediation - all with minimal human intervention.'
    )

    # ═══════════════════════════════════════════
    # 2. PROPOSED ARCHITECTURE OVERVIEW
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('2. High-Level Architecture')
    pdf.body_text(
        'The platform follows a layered, microservices-based architecture with six core layers. '
        'Each layer is independently scalable and communicates through well-defined interfaces.'
    )
    pdf.code_block(
        'Thousands of VMs (Log Sources)\n'
        '        |\n'
        '        v\n'
        '[Layer 1] Log Collection (Fluentd/Filebeat on each VM)\n'
        '        |\n'
        '        v\n'
        '[Layer 2] Message Queue (Apache Kafka - distributed streaming)\n'
        '        |\n'
        '        v\n'
        '[Layer 3] Stream + Batch Processing (Apache Flink / Spark)\n'
        '        |\n'
        '   +----+----+----+\n'
        '   v         v    v\n'
        '[Layer 4]  [Layer 4]  [Layer 4]\n'
        'Storage    Anomaly    Rule\n'
        '(ES/CH/S3) Detection  Engine\n'
        '           (ML)\n'
        '   +----+----+----+\n'
        '        v\n'
        '[Layer 5] Correlation + Root Cause Analysis Engine\n'
        '        |\n'
        '        v\n'
        '[Layer 6] Remediation Engine + Dashboard'
    )

    # ═══════════════════════════════════════════
    # 3. DATA INGESTION
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('3. Data Ingestion Layer')

    pdf.sub_title('Design Choice: Apache Kafka as Central Message Bus')
    pdf.body_text(
        'At ~1 TB/day from thousands of VMs, no single machine can handle the load. Apache Kafka '
        'provides a distributed, fault-tolerant message queue that acts as the backbone of the '
        'entire pipeline.'
    )
    pdf.sub_title('Why Kafka?')
    pdf.bold_bullet('High Throughput: ', 'Handles millions of messages per second across partitioned topics')
    pdf.bold_bullet('Durability: ', 'Messages are persisted to disk with configurable replication (factor of 3)')
    pdf.bold_bullet('Replay Capability: ', 'Consumers can re-read data from any offset - critical for reprocessing')
    pdf.bold_bullet('Multiple Consumers: ', 'Stream processor, batch processor, and archiver can all read independently')
    pdf.bold_bullet('Backpressure: ', 'Naturally handles traffic spikes without data loss')

    pdf.sub_title('Log Shippers: Fluentd / Filebeat')
    pdf.body_text(
        'Lightweight agents installed on every VM that tail log files, parse them, and forward '
        'to Kafka. They provide at-least-once delivery, buffering, and retry logic.'
    )

    pdf.sub_title('Two Processing Modes')
    w = [45, 45, 60]
    pdf.table_row(['Mode', 'Technology', 'Use Case'], w, header=True)
    pdf.table_row(['Real-time', 'Apache Flink', 'Immediate alerting, live anomaly detection'], w)
    pdf.table_row(['Batch', 'Apache Spark', 'Deep pattern mining, model training, reports'], w)

    # ═══════════════════════════════════════════
    # 4. LOG PROCESSING
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('4. Log Processing & Normalization')
    pdf.body_text(
        'Logs arrive in heterogeneous formats - syslog, JSON, plain text, CSV. The processing '
        'layer parses and normalizes all formats into a unified schema.'
    )

    pdf.sub_title('Example: Heterogeneous Input')
    pdf.code_block(
        '# Syslog format\n'
        'May 20 10:30:01 vm-1234 sshd[12345]: Failed password for root\n\n'
        '# JSON application log\n'
        '{"timestamp":"2026-05-20T10:30:00Z","level":"ERROR","msg":"DB timeout"}\n\n'
        '# Plain text\n'
        '[ERROR] 2026-05-20 10:30:00 - NullPointerException at UserService.java:142'
    )

    pdf.sub_title('Unified Output Schema')
    pdf.code_block(
        '{\n'
        '  "timestamp": "2026-05-20T10:30:00Z",\n'
        '  "source_host": "vm-1234",\n'
        '  "service": "auth-service",\n'
        '  "log_level": "ERROR",\n'
        '  "message": "DB connection timeout",\n'
        '  "metadata": {\n'
        '    "region": "us-east-1",\n'
        '    "deployment_version": "v2.3.1",\n'
        '    "cluster": "prod-cluster-a"\n'
        '  }\n'
        '}'
    )

    pdf.sub_title('Enrichment')
    pdf.body_text(
        'After parsing, logs are enriched with contextual metadata from external sources:'
    )
    pdf.bullet('Deployment metadata: Which version is running on this VM?')
    pdf.bullet('Topology data: What service dependency graph does this VM belong to?')
    pdf.bullet('Infrastructure metadata: Region, cluster, availability zone')

    # ═══════════════════════════════════════════
    # 5. DETECTION & ANALYSIS
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('5. Detection and Analysis')

    pdf.sub_title('A. Rule-Based Detection')
    pdf.body_text('Pattern matching for known issue categories:')
    pdf.bullet('Log level ERROR or FATAL -> immediate alert')
    pdf.bullet('HTTP 5xx status codes -> server error detected')
    pdf.bullet('Keywords: "OutOfMemoryError", "timeout", "connection refused"')
    pdf.bullet('Threshold breaches: CPU > 90%, disk > 95%, response time > 5s')

    pdf.sub_title('B. ML-Based Anomaly Detection')
    pdf.body_text('For issues not caught by static rules:')

    pdf.sub_sub_title('Isolation Forest')
    pdf.body_text(
        'Unsupervised algorithm that isolates anomalies by randomly partitioning data. '
        'Anomalous points (e.g., sudden error spikes) are isolated in fewer partitions. '
        'Used for detecting unusual log volume patterns.'
    )

    pdf.sub_sub_title('Autoencoders (Neural Networks)')
    pdf.body_text(
        'Trained to reconstruct "normal" log patterns. When a new log event cannot be '
        'reconstructed accurately (high reconstruction error), it is flagged as anomalous. '
        'Effective for detecting novel, previously unseen failure modes.'
    )

    pdf.sub_sub_title('Time-Series Analysis (LSTM)')
    pdf.body_text(
        'Monitors metrics derived from logs (error rates, latency trends) over time. '
        'Detects gradual degradation patterns like slowly increasing response times '
        'that rule-based systems miss.'
    )

    pdf.sub_sub_title('Log Clustering (NLP)')
    pdf.body_text(
        'Uses TF-IDF and embedding-based clustering to group similar log messages. '
        'Discovers new error categories automatically without manual rule creation.'
    )

    # ═══════════════════════════════════════════
    # 6. CORRELATION ENGINE
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('6. Correlation Engine')
    pdf.body_text(
        'A single incident often produces thousands of log entries across multiple services. '
        'The correlation engine links related events to form a unified incident view.'
    )

    pdf.sub_title('Correlation Strategies')

    pdf.sub_sub_title('1. Temporal Correlation')
    pdf.body_text(
        'Events within a configurable time window (e.g., 5 minutes) are grouped as potentially '
        'related. Uses sliding window algorithms for efficient real-time matching.'
    )

    pdf.sub_sub_title('2. Causal/Dependency Correlation')
    pdf.body_text(
        'Uses the service dependency graph: if Service A depends on B, and B fails, then '
        'A\'s errors are symptoms, not root causes. Traverses the graph to find the origin.'
    )

    pdf.sub_sub_title('3. Trace-Based Correlation')
    pdf.body_text(
        'Distributed tracing IDs (OpenTelemetry) link all logs from a single request across '
        'every service it passes through - providing end-to-end request visibility.'
    )

    pdf.sub_title('Example: Correlated Incident')
    pdf.code_block(
        '10:30:00 - Database:     "Disk space critical (98% full)"\n'
        '10:30:05 - Database:     "Write operation failed"\n'
        '10:30:06 - Auth Service: "DB connection timeout"\n'
        '10:30:07 - API Gateway:  "502 Bad Gateway from auth-service"\n'
        '10:30:07 - Frontend:     "User login failed"\n'
        '\n'
        'Root Cause: Database disk space -> all other errors are symptoms'
    )

    # ═══════════════════════════════════════════
    # 7. ROOT CAUSE ANALYSIS
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('7. Root Cause Analysis (RCA)')

    pdf.sub_title('Approach 1: Dependency Graph Traversal')
    pdf.body_text(
        'Build a directed graph of service dependencies (A -> B -> C -> DB). When multiple '
        'services fail, trace back to the deepest failing node in the dependency chain. '
        'That node is the most likely root cause.'
    )

    pdf.sub_title('Approach 2: Bayesian / Statistical Inference')
    pdf.body_text(
        'Calculate P(root_cause | observed_symptoms) using historical incident data. '
        'Example: "When auth-service and api-gateway both timeout, the database was the '
        'root cause 73% of the time in past incidents."'
    )

    pdf.sub_title('Approach 3: Historical Pattern Matching')
    pdf.body_text(
        'Compare the current incident fingerprint (set of correlated events) against a '
        'database of past incidents using similarity metrics. If the current pattern is '
        '92% similar to a past incident, surface that incident\'s root cause and resolution.'
    )

    pdf.sub_title('Code Mapping')
    pdf.body_text(
        'Once the root cause is identified, map it to source code:'
    )
    pdf.bullet('Stack trace parsing: extract file names, line numbers, function names')
    pdf.bullet('Repository indexing: link "UserService.java:142" to the actual code')
    pdf.bullet('Change correlation: check recent git commits to the failing module')

    # ═══════════════════════════════════════════
    # 8. REMEDIATION
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('8. Remediation & Resolution Assistance')

    pdf.sub_title('RAG-Based Recommendation Engine')
    pdf.body_text(
        'Uses Retrieval-Augmented Generation (RAG) to suggest fixes:'
    )
    pdf.code_block(
        '1. Store all past incident reports + resolutions in a vector database (FAISS)\n'
        '2. When new incident occurs, embed the incident description\n'
        '3. Retrieve top-K most similar past incidents\n'
        '4. Feed context to an LLM to generate remediation steps\n'
        '5. Present ranked recommendations to the operator'
    )

    pdf.sub_title('Types of Recommendations')
    pdf.bold_bullet('Configuration Fixes: ', '"Increase max_connections from 100 to 500 in db.conf"')
    pdf.bold_bullet('Operational Actions: ', '"Run docker system prune to free disk space"')
    pdf.bold_bullet('Code Changes: ', '"Add retry logic with exponential backoff in UserService.java:142"')
    pdf.bold_bullet('Infrastructure: ', '"Scale up database instance or add read replicas"')

    pdf.sub_title('Automated Validation')
    pdf.body_text(
        'Where applicable, trigger CI/CD pipelines to automatically test suggested fixes '
        'before deploying to production. Integration with Jenkins/GitHub Actions.'
    )

    # ═══════════════════════════════════════════
    # 9. STORAGE STRATEGY
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('9. Storage Strategy')

    pdf.sub_title('Tiered Storage Architecture')
    w2 = [30, 35, 35, 50]
    pdf.table_row(['Tier', 'Technology', 'Retention', 'Use Case'], w2, header=True)
    pdf.table_row(['Hot', 'Elasticsearch', '0-7 days', 'Fast full-text search, live queries'], w2)
    pdf.table_row(['Warm', 'ClickHouse', '7-30 days', 'Analytical queries, aggregations'], w2)
    pdf.table_row(['Cold', 'S3 / HDFS', '30+ days', 'Compressed archival, compliance'], w2)

    pdf.ln(3)
    pdf.sub_title('Why This Approach?')
    pdf.bullet('Hot tier (Elasticsearch): Optimized for real-time search and dashboards')
    pdf.bullet('Warm tier (ClickHouse): Columnar storage, 10x compression, fast analytical queries')
    pdf.bullet('Cold tier (S3): Cheapest storage, rarely accessed, used for compliance and ML training')

    pdf.sub_title('Data Lifecycle')
    pdf.code_block(
        'Log arrives -> Kafka -> Flink processes in real-time\n'
        '  -> Indexed in Elasticsearch (hot, 7 days)\n'
        '  -> After 7 days, migrated to ClickHouse (warm, 30 days)\n'
        '  -> After 30 days, compressed and archived to S3 (cold, indefinite)'
    )

    # ═══════════════════════════════════════════
    # 10. TECH STACK
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('10. Technology Stack')

    w3 = [40, 45, 65]
    pdf.table_row(['Layer', 'Technology', 'Justification'], w3, header=True)
    rows = [
        ('Log Collection', 'Fluentd / Filebeat', 'Lightweight, reliable log shippers'),
        ('Message Queue', 'Apache Kafka', 'High throughput, durability, replay'),
        ('Stream Processing', 'Apache Flink', 'Low latency, exactly-once semantics'),
        ('Batch Processing', 'Apache Spark', 'Large-scale analytics and ML training'),
        ('Hot Storage', 'Elasticsearch', 'Full-text search on recent logs'),
        ('Warm Storage', 'ClickHouse', 'Columnar DB for analytical queries'),
        ('Cold Storage', 'S3 / HDFS', 'Cost-effective archival'),
        ('Anomaly Detection', 'scikit-learn/PyTorch', 'Isolation Forest, Autoencoders'),
        ('Correlation', 'Neo4j', 'Dependency graph storage/traversal'),
        ('LLM / RAG', 'LLM + FAISS', 'Remediation suggestion generation'),
        ('Dashboard', 'Grafana / React', 'Real-time visualization'),
        ('Orchestration', 'Kubernetes', 'Container orchestration at scale'),
        ('CI/CD', 'Jenkins / GH Actions', 'Automated validation workflows'),
    ]
    for row in rows:
        pdf.table_row(row, w3)

    # ═══════════════════════════════════════════
    # 11. SCALABILITY
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('11. Scalability Considerations')

    pdf.sub_title('Horizontal Scaling Strategy')
    pdf.bold_bullet('Kafka: ', 'Add brokers + partitions as log volume grows')
    pdf.bold_bullet('Flink: ', 'Add task managers for parallel stream processing')
    pdf.bold_bullet('Elasticsearch: ', 'Add data nodes, use index lifecycle management')
    pdf.bold_bullet('ML Models: ', 'Multiple replicas behind a load balancer')

    pdf.sub_title('Estimated Resources (~1 TB/day)')
    w4 = [55, 50]
    pdf.table_row(['Component', 'Sizing'], w4, header=True)
    pdf.table_row(['Kafka Cluster', '5-10 brokers, 3x replication'], w4)
    pdf.table_row(['Flink Cluster', '10-20 task managers'], w4)
    pdf.table_row(['Elasticsearch', '5-10 data nodes, ~30 TB (7d)'], w4)
    pdf.table_row(['Total Platform', '~50-100 VMs'], w4)

    pdf.ln(3)
    pdf.sub_title('Reliability & Fault Tolerance')
    w5 = [50, 100]
    pdf.table_row(['Concern', 'Solution'], w5, header=True)
    pdf.table_row(['Log loss', 'Kafka durability + at-least-once delivery'], w5)
    pdf.table_row(['Processing failure', 'Flink checkpointing + auto-restart'], w5)
    pdf.table_row(['Storage node failure', 'ES/Kafka replication (factor 3)'], w5)
    pdf.table_row(['ML model failure', 'Multiple replicas + load balancer'], w5)
    pdf.table_row(['Network partition', 'Kafka handles natively; offset-based resume'], w5)

    # ═══════════════════════════════════════════
    # 12. PIPELINE SUMMARY
    # ═══════════════════════════════════════════
    pdf.add_page()
    pdf.section_title('12. End-to-End Pipeline Summary')
    pdf.code_block(
        'Step 1:  Ingest logs from distributed systems (Fluentd -> Kafka)\n'
        'Step 2:  Parse and normalize into unified schema (Flink)\n'
        'Step 3:  Detect errors, warnings, anomalies (Rules + ML)\n'
        'Step 4:  Correlate events across systems (Temporal + Causal + Trace)\n'
        'Step 5:  Root-cause analysis (Dependency graph + Bayesian + Historical)\n'
        'Step 6:  Identify impacted systems and components\n'
        'Step 7:  Map issues to source code areas (Stack traces + Git)\n'
        'Step 8:  Generate remediation recommendations (RAG + LLM)\n'
        'Step 9:  Trigger automated build/test validation (CI/CD)\n'
        'Step 10: Continuously learn from resolved incidents (Feedback loop)'
    )

    pdf.section_title('13. Conclusion')
    pdf.body_text(
        'This platform design addresses all functional requirements of the AI-driven log '
        'analysis problem through a layered, horizontally scalable architecture. Key design '
        'decisions include:'
    )
    pdf.bullet('Apache Kafka as the central nervous system for reliable, high-throughput ingestion')
    pdf.bullet('Dual processing modes (Flink streaming + Spark batch) for real-time and deep analysis')
    pdf.bullet('Hybrid detection using rule engines for known patterns and ML for novel anomalies')
    pdf.bullet('Multi-strategy correlation (temporal, causal, trace-based) for accurate incident grouping')
    pdf.bullet('Probabilistic RCA using dependency graphs, Bayesian inference, and historical matching')
    pdf.bullet('RAG-based remediation engine leveraging past incident resolutions')
    pdf.bullet('Tiered storage (ES/ClickHouse/S3) balancing query speed with cost efficiency')
    pdf.bullet('Continuous learning loop that improves diagnostics with each resolved incident')

    pdf.ln(5)
    pdf.body_text(
        'The architecture demonstrates competency across distributed systems design, data pipeline '
        'engineering, AI/ML integration, observability, scalability, reliability, and practical '
        'automation workflows - covering all evaluation areas specified in the problem statement.'
    )

    # Save
    output_path = '/Users/yashlohia/Major project/AI_Log_Analysis_Presentation.pdf'
    pdf.output(output_path)
    print(f'PDF saved to: {output_path}')

if __name__ == '__main__':
    generate()
