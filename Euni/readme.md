# 20290920_口試簡報與紙本
* [簡報](https://docs.google.com/presentation/d/1KqHiAt5G6GNHYqIcujSwUPhNh0k0r_ZerTcyCsG9nD4/edit?usp=sharing)
* [紙本](https://docs.google.com/document/d/1asEXGUFqOwFW7Q6wcRq7lSO9R9VBRkDj/edit?usp=sharing&ouid=109479015581701202828&rtpof=true&sd=true)

# 程式碼交接

## Data description
-ability2info.json ability 的name + description
-ability_info.pkl ability 對應的 technique

## Expanding Attack Data
### 1_expand_atk_dataset.ipynb
將 167 個 Attack Patterns 新增至 1000 個。
- Input: 
    - `./data/ability/ability2triplets.json` 原本一個 AP 只有一筆資料的檔案(新增前)
    - `./data/cate2ioc.json` 置換的 IOC 列表
- Output: 
  - `./data/ability/ability2triplets_expand.json` 新增後的攻擊資料（每個 AP 有 1000 筆資料），以 JOSN 格式存
  - `./data/ability/ability2triplets_expand.xlsx` 新增後的攻擊資料（每個 AP 有 1000 筆資料），以 xlsx 格式存
  
### 2_combine_atk_benign_triplets_to_one_set.ipynb
把前面新增後的攻擊資料和所有的 benign events 整合。變成一個 triplet set 之後做 embedding。
- Input: 
    - `./data/ability/ability2triplets_expand.json` #新增後的AP的EDs
    - `./data/ability/ability_info.pkl`
    - `./data/ability/benign_all_events_sorted.pkl` #benign ED
- Output: 
  - `./data/1_events/synthesize/benign_and_expand_atk_events.pkl`
  - `./data/2_triplets/synthesize/triplets.json` #benign + AP 的triplets
  - `./data/2_triplets/synthesize/tripletID_triplet_dict.json`
  - `./data/2_triplets/synthesize/tripletID_eventIDs_dict.json`

## Embedding
### 3_convert_to_openke_input.ipynb
把前面的 Triplet Set 轉成 OpenKE 要求的格式。
- Input: 
    - `./data/2_triplets/synthesize/triplets.json`
- Output: 
  - `./data/3_openKE/synthesize/train2id.txt` #openKE 要求
  - `./data/3_openKE/synthesize/valid2id.txt` #openKE 要求
  - `./data/3_openKE/synthesize/test2id.txt` #openKE 要求
  - `./data/3_openKE/synthesize/entity2id.txt` #openKE 要求
  - `./data/3_openKE/synthesize/relation2id.txt` #openKE 要求
  - `./data/3_openKE/synthesize/train2id_label.txt` #方便人工觀察該 Triplet 對應的 label
  - `./data/3_openKE/synthesize/valid2id_label.txt` #方便人工觀察該 Triplet 對應的 label
  - `./data/3_openKE/synthesize/test2id_label.txt` #方便人工觀察該 Triplet 對應的 label
  - `./data/3_openKE/synthesize/entity2id_objType.txt` #方便後續視覺化
  - `./data/3_openKE/synthesize/relation2id_type.txt` #方便後續視覺化
- 按openKE 要求，執行 `python3 n-n.py` 得到以下檔案
    - `1-1.txt`, `1-n.txt`, `n-1.txt`, `n-n.txt` #openKE 要求
    - `test2id_all.txt`, `type_constrain.txt` #openKE 要求

### 4_transE.ipynb / 4_transH.ipynb / 4_transR.ipynb
將文字轉成 embedding。檔案要保很久。每個檔案跑 5~10 小時。
- Input:
  - `./data/3_openKE/synthesize/*`
- Output:
  - `./data/4_embedding/synthesize/[MODEL]_[DIM].vec.json` #embedding 檔案
  - `./data/4_embedding/synthesize/model/[MODEL]_[DIM].ckpt` #embedding model


### 4_secureBERT_relation.ipynb / 4_secureBERT_entity.ipynb
- Enity
  -  Input:
     - `./data/3_openKE/synthesize/entity2id.txt`
     - `./data/3_openKE/synthesize/entity2id_objType.txt`
  - Output:
    - `./data/4_embedding/synthesize/secureBERT/embeddings_chunk_{i}.npy` #entity embedding 因為檔案較大，拆成小檔案存。
    - `./data/4_embedding/synthesize/model/secureBERT/entity/*` #entity embedding model
- Relation
  - Input:
    - `./data/3_openKE/synthesize/relation2id.txt`
    - `./data/3_openKE/synthesize/relation2id_type.txt`
  - Output
    - `./data/4_embedding/synthesize/secureBERT/relation.npy` #relation embedding
    - `./data/4_embedding/synthesize/model/secureBERT/relation/*` #relation embedding model

### 4_embedding_visualization.ipynb
- Input:
  - `./data/4_embedding/synthesize` # entity embedding path
  - `./data/3_openKE/synthesize/entity2id_objType.txt` # entity label
  - `./data/4_embedding/synthesize/secureBERT/relation.npy` # secureBERT relation embedding
  - `./data/3_openKE/synthesize/relation2id_type.txt` # relation label
- Output:
  - 圖顯示在檔案中
  
### 5_convert_to_apg_format.ipynb
前面都是以 Triplets 的形式存，這邊轉換成 APGs 的形式。除了 APG 本身，還會把周圍的 Benign 節點也加進來。
- Input:
  - `./data/3_openKE/synthesize/train2id.txt` 
  - `./data/3_openKE/synthesize/train2id_label.txt`
  - `./data/2_triplets/synthesize/tripletID_eventIDs_dict.json'` #因為有在新增 APG 的過程中，有些 triplet 是重複的，在前面做 openKE 的時候會被刪掉，這裡要把它復原回來。
- Output:
  - `data/5_APGs`
     
### 6_mlp.ipynb / 6_rnn.ipynb
- Input:
  - `./data/5_APGs` APGs
  -  `./data/4_embedding/synthesize/{MODEL_NAME}_{DIM}.vec.json` #每個 Triplet 的 Embedding
- Output:
  - `./data/6_prediction/synthesize/{mlp/rnn}/{MODEL_NAME}_{DIM}_classfication_report.xlsx`
  - `{OUTPUT_CLASSFICATION_REPORT_PATH}/{MODEL_NAME}_{DIM}_classfication_report_detail.xlsx`


## Deep Learning Model

## Sigma
### Data
有以下幾個資料夾與檔案：
* folder - source_rules
  * 這是從 [Sigma](https://github.com/SigmaHQ/sigma/tree/master/rules/windows) 下載下來的資料。
  * 20230323 和 20230708 為下載規則的日期，最後的研究結果是用 0708 的下載規則。
* folder - converted_rules
  * 經由 converter 轉換後的規則

### 0_statistics.ipynb
- 一些基本的統計
### 1_rule_converter.ipynb
- Input: Rules downloaded from Sigma github
    - `./Sigma/source_rules/[DATE]_downloaded/`
- Output: 
    - `./Sigma/converted_rules/[DATE]/json/rule_[i].json`
    - `./Sigma/converted_rules/[DATE]/yaml/rule_[i].yml`
    - `./Sigma/converted_rules/[DATE]/conversion_fail_fnames.csv` #轉換失敗的 rule 和原因
    - `./Sigma/converted_rules/[DATE]/fname_ruleCnt_dict.csv` # 各個 Sigma Rule 個被轉成幾個 detection rules
    - `./Sigma/converted_rules/[DATE]/ttp_ruleIdxs_dict.json` # 各個 TTP 對應到的 rule
    
### 2_rule_filter.ipynb
- Input:
    - `./Sigma/converted_rules/[DATE]/json/rule_[i].json`
    - `./Sigma/RuleAttr_SynthesizedAttr_Map.yml` #事先定義好的屬性對照表(Synthesize)
- Output: 
    - `./Sigma/filtered_rule_idx/[DATE]/valid_rids_for_any_dataset.txt` # 可以適用於所有 log dataset 的 rule
    - `./Sigma/filtered_rule_idx/[DATE]/useful_rids_for_synthesize/` # 可以用於 synthesized dataset 的 rules
        - `stable.txt`
        - `experiment.txt`
        - `test.txt`
        - `all.txt` 
        
### 3_rule_matcher_synthesize.py
- Input:
    - Rule: `./Sigma/converted_rules/{DATE}/yaml/*`
    - `./Sigma/filtered_rule_idx/{DATE}/useful_rids_for_synthesize/{all/experimental/test}.txt`
    - `./Sigma/RuleAttr_SynthesizedAttr_Map.yml`
    - Triplets: `./data/1_triplets/synthesize/triplets.json` or Events ``
- Output:
    - `./Sigma/matching_result/{RULE_DATE}_{RULE_TYPE}/synthesize`
        - `eid_matchedTtps_dict.json`
        - `rid_matchEventIdx.json`
        - `eid_yTrue_dict.json`
        - `chunk_args.pkl`
        
### 4_result.ipynb
