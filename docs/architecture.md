```mermaid
graph TB
    %% User Interface Layer
    subgraph "User Interface Layer"
        UI[Streamlit UI<br/>snapshot_viewer.py]
        CLI[CLI Manager<br/>snapshot_manager.py]
        JUPYTER[Jupyter Notebooks<br/>demo.ipynb, amazon_strategy.ipynb]
    end

    %% Core Application Layer
    subgraph "Core Application Layer"
        BDF[BrightDataFilter<br/>brightdata_filter.py]
        FC[Filter Criteria<br/>filter_criteria.py]
        DR[Dataset Registry<br/>dataset_registry.py]
        CM[Config Manager<br/>config.py]
    end

    %% Data Storage Layer
    subgraph "Data Storage Layer"
        SR[Snapshot Records<br/>snapshot_records/*.json]
        DL[Downloads<br/>downloads/*.json]
        SEC[Secrets<br/>secrets.yaml]
        DS[Dataset Schemas<br/>datasets/*.md]
    end

    %% External API Layer
    subgraph "External API Layer"
        BDA[BrightData API<br/>api.brightdata.com]
        FILTER[Filter Endpoint<br/>/datasets/filter]
        SNAPSHOT[Snapshot Endpoint<br/>/datasets/snapshots]
        DOWNLOAD[Download Endpoint<br/>/datasets/snapshots/{id}/content]
    end

    %% Dataset Support
    subgraph "Supported Datasets"
        AMAZON[Amazon Products<br/>gd_l7q7dkf244hwjntr0]
        AMAZON_WALMART[Amazon-Walmart<br/>gd_m4l6s4mn2g2rkx9lia]
        SHOPEE[Shopee Products<br/>gd_lk122xxgf86xf97py]
    end

    %% User Interactions
    UI --> BDF
    CLI --> BDF
    JUPYTER --> BDF

    %% Core Dependencies
    BDF --> FC
    BDF --> DR
    BDF --> CM
    FC --> DR

    %% Data Flow
    BDF --> SR
    BDF --> DL
    CM --> SEC
    DR --> DS

    %% API Communication
    BDF --> BDA
    BDA --> FILTER
    BDA --> SNAPSHOT
    BDA --> DOWNLOAD

    %% Dataset Integration
    DR --> AMAZON
    DR --> AMAZON_WALMART
    DR --> SHOPEE

    %% Key Features
    subgraph "Key Features"
        DEDUP[Smart Deduplication<br/>Prevents duplicate queries]
        VALID[Type-Aware Validation<br/>Runtime field validation]
        MONITOR[Real-time Monitoring<br/>Status tracking]
        DOWNLOAD_MGR[Download Management<br/>Cost-aware downloads]
    end

    BDF --> DEDUP
    FC --> VALID
    BDF --> MONITOR
    BDF --> DOWNLOAD_MGR

    %% Styling
    classDef uiLayer fill:#e1f5fe
    classDef coreLayer fill:#f3e5f5
    classDef dataLayer fill:#e8f5e8
    classDef apiLayer fill:#fff3e0
    classDef datasetLayer fill:#fce4ec
    classDef featureLayer fill:#f1f8e9

    class UI,CLI,JUPYTER uiLayer
    class BDF,FC,DR,CM coreLayer
    class SR,DL,SEC,DS dataLayer
    class BDA,FILTER,SNAPSHOT,DOWNLOAD apiLayer
    class AMAZON,AMAZON_WALMART,SHOPEE datasetLayer
    class DEDUP,VALID,MONITOR,DOWNLOAD_MGR featureLayer
```
