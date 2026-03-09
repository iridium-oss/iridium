# Federated Learning Partitioning

Partition strategies, manifest schema, and quality checks for IRIDIUM FL.

## Partition Strategies

| Strategy | Description | Use |
|----------|-------------|-----|
| by_district | One partition per district (geography). | Real product logic; district-level signals. |
| by_provider | One partition per operator or data provider. | Operator-held data. |
| by_source_family | Partition by source family (e.g. metro, bus, road). | Source-aligned FL. |
| by_time_block | Partition by time window. | Simulation or temporal studies. |
| synthetic_institution | Arbitrary grouping for simulation. | Simulation only; manifest marks simulation_only and synthetic. |

No raw central merge is required; each partition is self-contained.

## Manifest Schema

Each partition has a manifest (e.g. `{partition_id}_manifest.json`) with:

- **partition_id**: Unique ID (e.g. p_by_district_0).
- **strategy**: One of the enum values above.
- **coverage_interval_start**, **coverage_interval_end**: Optional ISO datetime/date.
- **source_types**: List of source types (e.g. metro, bus).
- **label_availability**: full | partial | none.
- **sample_count**: Number of samples.
- **missingness_pct**: Optional 0 to 100.
- **geography**: Optional district or region code.
- **metadata**: Extra fields (e.g. simulation_only, synthetic for synthetic_institution).
- **version**: Manifest schema version.

## Partition Data

Data files (e.g. `{partition_id}_data.npz`) contain at least:

- **x**: Feature matrix (float32), shape (n, feature_dim).
- **y**: Target matrix (float32), shape (n, output_dim).

Generated partitions use this format. Real data pipelines must produce the same schema and align feature_dim with the model (e.g. 8).

## Partition Quality Checks

- **Minimum samples**: Clients require a minimum number of samples (e.g. 10) to train; otherwise they return insufficient_data.
- **Manifest validation**: Pydantic PartitionManifest validates manifest files on load.
- **Drift or heterogeneity**: Summaries (e.g. per-partition sample counts, source_types) are in the manifest; no automatic drift detection in the baseline.

## Versioning

Partition manifests and data should be versioned (e.g. dataset version, feature version) so that FL runs can reference them. Link artifacts to git commit, dataset version, and partition strategy in docs and run metadata.
