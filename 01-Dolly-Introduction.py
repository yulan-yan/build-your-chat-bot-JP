# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC # オープンモデルとDatabricks LakehouseでChatGPTの魔法を民主化する。
# MAGIC
# MAGIC <img style="float:right" width="400px" src="https://raw.githubusercontent.com/databricks-demos/dbdemos-resources/main/images/product/llm-dolly/llm-dolly.png">
# MAGIC
# MAGIC 大規模言語モデルは、まるで知能があるかのようにチャットしたり、質問に答えたりして、驚くべき結果をもたらします。
# MAGIC
# MAGIC しかし、どうすればLLMに特定のデータセットに関する質問に答えさせることができるのでしょうか？あなたの会社のナレッジベース、ドキュメント、Slackのチャットに基づいた質問に答えることを想像してみてください。
# MAGIC
# MAGIC オープンソースのツールやオープンなLLMを活用すれば、Databricksで簡単に構築することができます。
# MAGIC
# MAGIC ## Databricks Dolly： 世界初の真にオープンな命令チューニングLLM
# MAGIC
# MAGIC 現在のところ、最先端のモデルのほとんどは、制限付きのライセンスで提供されており、商業目的で使用することはできません。これは、オープンでないデータセットを使って学習や微調整が行われたためです。
# MAGIC
# MAGIC この課題を解決するために、DatabricksはDollyをリリースしました。Dollyは初の真にオープンなLLMです。Dollyは、`databricks-dolly-15k`（大規模言語モデルのインストラクションチューニング用に特別に設計された、人間が生成した高品質のプロンプト/レスポンスのペア15,000）を使用してファインチューニングされているため、独自の商用モデルを作るための出発点として使用することができます。
# MAGIC
# MAGIC ## LLMs on Databricks
# MAGIC このデモではDollyの`databricks-dolly-15k`データセットでファインチューニングされたオープンモデルmosaicml/mpt-7b-instruct を利用します。
# MAGIC Databricksに関する日本語のQ＆Aデータセットを使用してプロンプトエンジニアリングを行います。

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## ユーザーのDatabricksに関する質問に答えてくれる日本語版AI Assistantの構築
# MAGIC
# MAGIC このデモでは、mosaicml/mpt-7b-instructをベースとしたチャットボットを作成する予定です。アプリケーションにボットを追加して、ユーザーのDatabricksに関する質問に答えたいと思います。
# MAGIC
# MAGIC このデモは2つのセクションに分かれています：
# MAGIC
# MAGIC - 1/ **データ準備**: Q&Aデータセットの取り込みとクリーニングを行い、ベクトルデータベースへの埋め込みとして変換する。
# MAGIC - 2/ **Q&A推論**：Q&AをDollyの追加コンテキストとして活用し、Dollyがクエリーに回答します。これは「プロンプトエンジニアリング」とも呼ばれます。
# MAGIC
# MAGIC <img style="margin: auto; display: block" width="1200px" src="https://github.com/yulan-yan/images-public/blob/6551b258815ed74ec5f54db34b6129e6325aa941/dolly-dbqa-chatbot.png?raw=true">

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ## 1/ Databricks Lakehouseによるデータ準備とVectorデータベース作成
# MAGIC
# MAGIC
# MAGIC <img style="float: right" width="500px" src="https://github.com/yulan-yan/images-public/blob/6551b258815ed74ec5f54db34b6129e6325aa941/dolly_dataPrep.png?raw=true">
# MAGIC
# MAGIC チャットボット作成で最も難しいのは、データの収集、準備、クリーニングです。
# MAGIC
# MAGIC Databricks Lakehouseは、これをシンプルに実現します！Delta Lake、Delta Live Table、Databricks特化の実行オンジンを活用することで、シンプルなデータパイプラインを構築し、パイプラインのTCOを劇的に削減することができます

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC [02-Data-preparation]($./02-Data-preparation)ノートブックを開き、データを取り込み、ベクトルデータベースの構築を開始します。

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ## 2/ Q&Aのためのプロンプトエンジニアリング
# MAGIC
# MAGIC <img style="float: right" width="500px" src="https://github.com/yulan-yan/images-public/blob/6551b258815ed74ec5f54db34b6129e6325aa941/dolly_QAinference.png?raw=true">
# MAGIC
# MAGIC Q&Aデータセットが準備できるようになったので、Dollyを活用して質問に答えることができます。
# MAGIC
# MAGIC 簡単な質問と回答のプロセスから始めます。
# MAGIC
# MAGIC * ユーザーから質問を投げます
# MAGIC * Q&Aデータセットから類似コンテンツを取得します
# MAGIC * コンテンツをコンテキストとしてプロンプトに追加します
# MAGIC * プロンプトをDollyに送信します
# MAGIC * ユーザーへ回答を表示します

# COMMAND ----------

# MAGIC %md
# MAGIC 次の [03-Q&A-prompt-engineering]($./03-Q&A-prompt-engineering) ノートを開いて、`langchain`を使ってモデルへ送信するプロンプトを改善し、ユーザーの質問をDollyに送り、よりいい答えを得る方法を学びましょう。

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ## 3/ チャットボットのためのプロンプトエンジニアリング
# MAGIC
# MAGIC <img style="float: right" width="600px" src="https://github.com/yulan-yan/images-public/blob/6551b258815ed74ec5f54db34b6129e6325aa941/dolly_conversation.png?raw=true">
# MAGIC
# MAGIC ボットの能力を高めて、チャットボットとして動作するようにしましょう。
# MAGIC
# MAGIC この例では、複数の質問と回答の連鎖を可能にすることで、ボットを改良します。
# MAGIC
# MAGIC 以前の動作（Q&Aデータセットからコンテキストをプロンプトに追加する）はそのままに、各質問の間にメモリを追加するようにします。
# MAGIC
# MAGIC 中間モデルと `langchain` `ConversationSummaryMemory` オブジェクトを活用して、進行中のやり取りを要約し、プロンプトをコントロールしておきましょう！

# COMMAND ----------

# MAGIC %md
# MAGIC 次の [04-chat-bot-prompt-engineering]($./04-chat-bot-prompt-engineering) ノートを開き、チャットボットを作成します！

# COMMAND ----------

# MAGIC %md 
# MAGIC
# MAGIC ## 4/ Dollyをファインチューニングする
# MAGIC
# MAGIC 自分のデータセットを持っていて、dollyの回答方法に特化させたい場合は、LLMを自分の要件に合わせてファインチューニングすることができます！
# MAGIC
# MAGIC これはより高度な要件であり、特定のチャットフォーマットとフォーマットされたデータセットで答えるようにDollyを特化させるのに便利です、例えば：
# MAGIC
# MAGIC ```
# MAGIC AI: 私はDatabricks AI アシスタントです、何かお手伝いできることはありますか？
# MAGIC 人間：AutoMLでサポートしている分類モデルのアルゴリズムは何ですか？
# MAGIC AI：Decision trees、Random forests、Logistic regression、XGBoost、LightGBM
# MAGIC 人間：構築したモデルの予測に対して解釈できますか？
# MAGIC AI：はい、AutoMLの回帰、分類ランによって生成されるノートブックには、Shapley値を計算するコードが含まれています。Shapley値はゲーム理論に基づいており、モデルの予測に対するそれぞれの特徴量の重要度を推定します。
# MAGIC ...
# MAGIC ```
# MAGIC
# MAGIC Dollyは現在活発に開発が進められているため、最新のファインチューニング例として公式の[dollyリポジトリ](https://github.com/databrickslabs/dolly)を検索することをお勧めします！
