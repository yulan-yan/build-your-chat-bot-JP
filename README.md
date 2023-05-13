# build-your-chat-bot-JP

このデモではDollyのdatabricks-dolly-15kデータセットでファインチューニングされたオープンモデルmosaicml/mpt-7b-instruct を利用します。 

Databricksに関する日本語のQ＆Aデータセットを使用してプロンプトエンジニアリングを行います。

## ユーザーのDatabricksに関する質問に答えてくれる日本語版AI Assistantの構築

このデモでは、mosaicml/mpt-7b-instructをベースとしたチャットボットを作成する例です。アプリケーションにボットを追加して、ユーザーのDatabricksに関する質問に答えたいと思います。

このデモは2つのセクションに分かれています：

- 1/ **データ準備**: Q&Aデータセットの取り込みとクリーニングを行い、ベクトルデータベースへの埋め込みとして変換する。
- 2/ **Q&A推論**：Q&AをDollyの追加コンテキストとして活用し、Dollyがクエリーに回答します。これは「プロンプトエンジニアリング」とも呼ばれます。

<img style="margin: auto; display: block" width="1200px" src="https://github.com/yulan-yan/images-public/blob/6551b258815ed74ec5f54db34b6129e6325aa941/dolly-dbqa-chatbot.png?raw=true">

## 3/ チャットボットのためのプロンプトエンジニアリング

<img style="float: right" width="600px" src="https://github.com/yulan-yan/images-public/blob/6551b258815ed74ec5f54db34b6129e6325aa941/dolly_conversation.png?raw=true">

さらに、ボットの能力を高めて、チャットボットとして動作するまで実装しています。

この例では、複数の質問と回答の連鎖を可能にすることで、ボットを改良します。

以前の動作（Q&Aデータセットからコンテキストをプロンプトに追加する）はそのままに、各質問の間にメモリを追加するようにします。

中間モデルと `langchain` `ConversationSummaryMemory` オブジェクトを活用して、進行中のやり取りを要約し、プロンプトをコントロールいく例となります。
