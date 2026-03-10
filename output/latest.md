# Paper Radar Digest

- window: last 7 days
- shown: 12

## 精读样板

- WiscKey 精读样板：见 `wisckey-analysis.html`

## 顶会 / 经典白名单池

### 白名单-1. WiscKey: Separating Keys from Values in SSD-Conscious Storage
- venue: FAST 2016；storage, kv, lsm
- tags: FAST-style
- take: 键值分离的代表作，LSM/SSD 方向绕不过去。

### 白名单-2. Monkey: Optimal Navigable Key-Value Store
- venue: SIGMOD 2017；storage, lsm, filters
- tags: FAST-style
- take: LSM 读放大与布隆过滤器分配的经典工作。

### 白名单-3. PebblesDB: Building Key-Value Stores using Fragmented Log-Structured Merge Trees
- venue: SOSP 2017；storage, kv, lsm
- tags: FAST-style
- take: LSM 结构改造的代表作，适合和 WiscKey 对照着看。

### 白名单-4. Titan: A High-Performance Remote-Swap System
- venue: FAST 2020；storage, memory, systems
- tags: FAST-style, HPCA-style, OSDI/ATC/EuroSys-style
- take: FAST 味很正，系统与存储交叉。

### 白名单-5. Design Tradeoffs for SSD Performance
- venue: USENIX ATC 2008；storage, ssd
- tags: FAST-style
- take: SSD 设计空间的老经典。

### 白名单-6. Learned Cache Replacement for Datacenter Storage Systems
- venue: OSDI 2020；storage, systems, cache
- tags: FAST-style, OSDI/ATC/EuroSys-style
- take: 系统味较强，数据中心存储方向。

### 白名单-7. The Tail at Scale
- venue: CACM 2013；systems, datacenter, latency
- tags: OSDI/ATC/EuroSys-style
- take: 系统性能分析与延迟思维的必读经典。

### 白名单-8. A Case for Tiny Tasks in Compute Clusters
- venue: HotOS 2013；systems, datacenter
- tags: OSDI/ATC/EuroSys-style
- take: 系统基础设施调度思路的经典小文。

### 白名单-9. Optimizing Datacenter Performance via CXL-Aware Memory Tiering
- venue: HPCA 2024；architecture, memory, cxl
- tags: HPCA-style
- take: 偏你感兴趣的内存/架构/CXL 路线。

### 白名单-10. BetrFS: A Right-Optimized Write-Optimized File System
- venue: FAST 2015；storage, filesystem
- tags: FAST-style
- take: 写优化文件系统的代表性工作。

### 白名单-11. SILK: Preventing Latency Spikes in Log-Structured Merge Key-Value Stores
- venue: FAST 2019；storage, kv, lsm
- tags: FAST-style
- take: LSM 延迟毛刺问题，非常贴近工程痛点。

### 白名单-12. LOCATOR: A Key-Value Store for Hybrid-Cloud Workloads
- venue: FAST 2023；storage, systems, kv
- tags: FAST-style, OSDI/ATC/EuroSys-style
- take: 更现代的存储系统视角。

### 白名单-13. Tpp: Transparent Page Placement for CXL-Enabled Tiered-Memory
- venue: HPCA 2024；architecture, memory, cxl
- tags: HPCA-style
- take: CXL 分层内存方向，挺对你胃口。

### 白名单-14. RowClone: Fast and Energy-Efficient In-DRAM Bulk Data Copy and Initialization
- venue: MICRO 2013；architecture, memory
- tags: HPCA-style
- take: 内存系统经典，适合和现代 memory tiering 一起看。

### 白名单-15. SoftMC: A Flexible and Practical Open-Source Infrastructure for Enabling Experimental DRAM Studies
- venue: HPCA 2017；architecture, memory
- tags: HPCA-style
- take: 偏架构实验基础设施，味道很正。

## Zotero 经典相关论文

### 经典-1. WiscKey: Separating Keys from Values in SSD-Conscious Storage
- score: 35
- tags: FAST-style
- why: FAST-style；来自 Zotero 现有论文池
- take: 这类更像你的长期主线，适合精读和做研究借鉴。

### 经典-2. HotRAP: Hot Record Retention and Promotion for LSM-trees with Tiered Storage
- score: 31
- tags: FAST-style, HPCA-style
- why: FAST-style；HPCA-style；来自 Zotero 现有论文池
- take: 这类更像你的长期主线，适合精读和做研究借鉴。

### 经典-3. SimpleSSD: Modeling Solid State Drives for Holistic System Simulation
- score: 30
- tags: FAST-style, HPCA-style, Systems
- why: FAST-style；HPCA-style；Systems；来自 Zotero 现有论文池
- take: 这类更像你的长期主线，适合精读和做研究借鉴。

## 必看

### 必看-1. Mozart: Modularized and Efficient MoE Training on 3.5D Wafer-Scale Chiplet Architectures
- score: 34
- tags: HPCA-style, OSDI/ATC/EuroSys-style, AI Infra
- why: +7 chiplet；+6 moe；+3 recent；+2 cat:cs.AR；canon:The Tail at Scale / Optimizing Datacenter Performance via CXL-Aware Memory Tiering / Tpp: Transparent Page Placement for CXL-Enabled Tiered-Memory
- take: 偏内存/架构味，值得看是不是有真货而不是只会画图。
- link: https://arxiv.org/abs/2603.07006v1
- pdf: https://arxiv.org/pdf/2603.07006v1.pdf
- analysis: ./analysis/mozart-modularized-and-efficient-moe-training-on-3-5d-wafer-scale-chiple.html

### 必看-2. Scheduling Parallel Optical Circuit Switches for AI Training
- score: 33
- tags: HPCA-style, OSDI/ATC/EuroSys-style, DAC/ICCAD-style, AI Infra
- why: +6 datacenter；+6 moe；+3 recent；canon:Optimizing Datacenter Performance via CXL-Aware Memory Tiering / RowClone: Fast and Energy-Efficient In-DRAM Bulk Data Copy and Initialization / SoftMC: A Flexible and Practical Open-Source Infrastructure for Enabling Experimental DRAM Studies
- take: AI infra 方向，但得警惕是不是只是模型套壳。
- link: https://arxiv.org/abs/2603.07373v1
- pdf: https://arxiv.org/pdf/2603.07373v1.pdf
- analysis: ./analysis/scheduling-parallel-optical-circuit-switches-for-ai-training.html

### 必看-3. Explainable and Hardware-Efficient Jamming Detection for 5G Networks Using the Convolutional Tsetlin Machine
- score: 28
- tags: OSDI/ATC/EuroSys-style, AI Infra
- why: +5 latency；+7 inference；+3 recent；+2 cat:cs.AR；canon:Titan: A High-Performance Remote-Swap System / Design Tradeoffs for SSD Performance / The Tail at Scale
- take: 偏内存/架构味，值得看是不是有真货而不是只会画图。
- link: https://arxiv.org/abs/2603.07336v1
- pdf: https://arxiv.org/pdf/2603.07336v1.pdf
- analysis: ./analysis/explainable-and-hardware-efficient-jamming-detection-for-5g-networks-usi.html

### 必看-4. Configurable Runtime Orchestration for Dynamic Data Retrieval in Distributed Systems
- score: 27
- tags: OSDI/ATC/EuroSys-style
- why: +7 distributed system；+5 latency；+3 recent；+2 cat:cs.DC；canon:Titan: A High-Performance Remote-Swap System / The Tail at Scale / A Case for Tiny Tasks in Compute Clusters
- take: 先扫摘要和实验，别被标题党骗了。
- link: https://arxiv.org/abs/2603.06980v1
- pdf: https://arxiv.org/pdf/2603.06980v1.pdf
- analysis: ./analysis/configurable-runtime-orchestration-for-dynamic-data-retrieval-in-distrib.html

### 必看-5. A Miniature Brain Transformer: Thalamic Gating, Hippocampal Lateralization, Amygdaloid Salience, and Prefrontal Working Memory in Attention-Coupled Latent Memory
- score: 27
- tags: FAST-style
- why: +7 persistent memory；+1 zotero:persistent；+3 recent；canon:Optimizing Datacenter Performance via CXL-Aware Memory Tiering / Tpp: Transparent Page Placement for CXL-Enabled Tiered-Memory / RowClone: Fast and Energy-Efficient In-DRAM Bulk Data Copy and Initialization
- take: 偏内存/架构味，值得看是不是有真货而不是只会画图。
- link: https://arxiv.org/abs/2603.07217v1
- pdf: https://arxiv.org/pdf/2603.07217v1.pdf
- analysis: ./analysis/a-miniature-brain-transformer-thalamic-gating-hippocampal-lateralization.html

## 可扫

### 可扫-1. VLN-Cache: Enabling Token Caching for VLN Models with Visual/Semantic Dynamics Awareness
- score: 20
- tags: HPCA-style, AI Infra
- why: +5 cache；+7 inference；-4 vision-language；+3 recent
- take: 偏内存/架构味，值得看是不是有真货而不是只会画图。
- link: https://arxiv.org/abs/2603.07080v1
- pdf: https://arxiv.org/pdf/2603.07080v1.pdf
- analysis: ./analysis/vln-cache-enabling-token-caching-for-vln-models-with-visual-semantic-dyn.html

### 可扫-2. Efficient Personalized Reranking with Semi-Autoregressive Generation and Online Knowledge Distillation
- score: 17
- tags: AI Infra
- why: +5 latency；+7 inference；+3 recent；canon:Titan: A High-Performance Remote-Swap System / The Tail at Scale / BetrFS: A Right-Optimized Write-Optimized File System
- take: AI infra 方向，但得警惕是不是只是模型套壳。
- link: https://arxiv.org/abs/2603.07107v1
- pdf: https://arxiv.org/pdf/2603.07107v1.pdf
- analysis: ./analysis/efficient-personalized-reranking-with-semi-autoregressive-generation-and.html

### 可扫-3. SuperSkillsStack: Agency, Domain Knowledge, Imagination, and Taste in Human-AI Design Education
- score: 17
- tags: HPCA-style, DAC/ICCAD-style
- why: +6 accelerator；-5 education；+3 recent；canon:Tpp: Transparent Page Placement for CXL-Enabled Tiered-Memory
- take: 先扫摘要和实验，别被标题党骗了。
- link: https://arxiv.org/abs/2603.07016v1
- pdf: https://arxiv.org/pdf/2603.07016v1.pdf
- analysis: ./analysis/superskillsstack-agency-domain-knowledge-imagination-and-taste-in-human-.html

### 可扫-4. Foundational World Models Accurately Detect Bimanual Manipulator Failures
- score: 14
- tags: OSDI/ATC/EuroSys-style, AI Infra
- why: +6 data center；+3 recent；canon:Titan: A High-Performance Remote-Swap System
- take: AI infra 方向，但得警惕是不是只是模型套壳。
- link: https://arxiv.org/abs/2603.06987v1
- pdf: https://arxiv.org/pdf/2603.06987v1.pdf
- analysis: ./analysis/foundational-world-models-accurately-detect-bimanual-manipulator-failure.html

## 先别看

### 先别看-1. AutoDataset: A Lightweight System for Continuous Dataset Discovery and Search
- score: 13
- tags: AI Infra
- why: +5 latency；+7 inference；+3 recent；canon:PebblesDB: Building Key-Value Stores using Fragmented Log-Structured Merge Trees / SILK: Preventing Latency Spikes in Log-Structured Merge Key-Value Stores / SoftMC: A Flexible and Practical Open-Source Infrastructure for Enabling Experimental DRAM Studies
- take: AI infra 方向，但得警惕是不是只是模型套壳。
- link: https://arxiv.org/abs/2603.07271v1
- pdf: https://arxiv.org/pdf/2603.07271v1.pdf
- analysis: ./analysis/autodataset-a-lightweight-system-for-continuous-dataset-discovery-and-se.html

### 先别看-2. AIReSim: A Discrete Event Simulator for Large-scale AI Cluster Reliability Modeling
- score: 13
- tags: OSDI/ATC/EuroSys-style
- why: +3 recent；+2 cat:cs.DC；canon:Titan: A High-Performance Remote-Swap System / Design Tradeoffs for SSD Performance / A Case for Tiny Tasks in Compute Clusters
- take: 先扫摘要和实验，别被标题党骗了。
- link: https://arxiv.org/abs/2603.07041v1
- pdf: https://arxiv.org/pdf/2603.07041v1.pdf
- analysis: ./analysis/airesim-a-discrete-event-simulator-for-large-scale-ai-cluster-reliabilit.html

### 先别看-3. Improving reasoning at inference time via uncertainty minimisation
- score: 10
- tags: OSDI/ATC/EuroSys-style, AI Infra
- why: +7 inference；+3 recent；canon:Titan: A High-Performance Remote-Swap System / SoftMC: A Flexible and Practical Open-Source Infrastructure for Enabling Experimental DRAM Studies
- take: AI infra 方向，但得警惕是不是只是模型套壳。
- link: https://arxiv.org/abs/2603.07159v1
- pdf: https://arxiv.org/pdf/2603.07159v1.pdf
- analysis: ./analysis/improving-reasoning-at-inference-time-via-uncertainty-minimisation.html
