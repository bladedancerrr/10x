# 10X Dumping Ground

Keep 10X notes, reports, results, (small) datasets etc. as you wish.
Basically instead of dumping everything in the
[Google doc](https://docs.google.com/document/d/1EhqPusGRCDKdK5tx5RpEhgwj_LCAi7plb2B62VvbaG4/edit),
feel free to dump it in here.

## Data Paths

| Description                      | Path                                                                    | Cluster   |
| ----------------------           | ----------------------------------------------------------------------- | --------- |
| NA12878 WGS from [10X][1]        | `/data/cephfs/punim0010/data/External/Reference/NA12878-10x-2018/wfu`   | Spartan   |
| NA12878 WGS from [10X][1] re-run | `/data/cephfs/punim0010/projects/10X_WGS-test`                          | Spartan   |
| NA12878 WGS from [10X][1] re-run | `/g/data3/gx8/projects/Hsu_10X_WGS/NA12878-10X-WFU`                     | Raijin    |
| LongRanger + References          | `/data/projects/punim0010/opt/`                                         | Spartan   |


[1]: https://support.10xgenomics.com/de-novo-assembly/datasets/2.0.0/wfu

## Tools

| Name             | Description                                                               | Notes |
|------------------+---------------------------------------------------------------------------+-------|
| [bxtools][bxt]   |                                                                           |       |
| [longranger][lr] | 10X pipeline for WGS/WES read alignment, SNP/Indel/SV calling and phasing |       |
| [HapCut2][hc2]   |                                                                           |       |

[bxt]: https://github.com/walaj/bxtools
[lr]: https://support.10xgenomics.com/genome-exome/software/pipelines/latest/what-is-long-ranger
[hc2]: https://github.com/vibansal/HapCUT2
