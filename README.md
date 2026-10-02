# GitHub Change Management MVP

公開デモ専用の架空サンプルです。実在の案件情報・本番資格情報は含みません。送料計算の小さな変更を使い、Issue → PR → CI → リリースタグ → staging検証 → 承認待ち → 反映記録の流れを示します。

[Project](https://github.com/users/omitsuhashi/projects/12) · [Issues](https://github.com/omitsuhashi/github-change-management-mvp-20261002/issues) · [Pull requests](https://github.com/omitsuhashi/github-change-management-mvp-20261002/pulls) · [Actions](https://github.com/omitsuhashi/github-change-management-mvp-20261002/actions)

## 試し方

1. Issueフォームで目的・変更内容・受け入れ条件を登録します。
2. 作業ブランチからPRを作り、Issueを `Refs #番号` で参照します。
3. `python3 -m unittest -v` がCIでも実行されます。テスト失敗・必須レビュー不足はマージを止めます。
4. main上のコミットへ `v1.0.0` 等のタグを作成します。指定発行者以外の作成、既存タグの移動・削除を制限します。
5. Release demoが一度だけ成果物を作り、staging検証記録とSHA-256を保存します。
6. production-demoはEnvironmentの承認待ちになります。承認後に同じ成果物を検証し、Runner上で反映を模擬して結果をartifactへ保存します。実サーバーへのデプロイは行いません。

## 設定する保護

- main: PR必須、CIの `test` 必須、レビュー1名、差分変更時の承認失効、CODEOWNERSレビュー、会話の解決、force push・削除禁止。通常のbypassはありません。
- 正式タグ: 作成制限と更新・削除制限を別Rulesetにします。個人所有Repositoryのため、作成はRepository Adminに限定し、移動・削除側にはbypassを設けません。
- production-demo: `v*` タグだけ許可、必須承認者 `omitsuhashi`、自己承認防止、管理者による承認bypass禁止。
- Actions: 使用Actionを限定し完全なcommit SHAで固定。Tokenはreadを基本にします。Secretやクラウド接続は設定しません。

## レビュー・承認に必要なユーザー

このRepositoryは個人所有です。CODEOWNERSは所有者を設定していますが、所有者が作成したPRを本人は承認できません。実演を先へ進めるには、別のレビュー担当者へWrite権限を付与し、必要に応じてCODEOWNERSを更新してください。

production-demoも起動者の自己承認を禁止します。所有者がタグを作った実行は所有者だけでは承認できません。別の承認者の登録か、別の担当者による開始が必要です。デモを通すためにこの保護を外しません。

## Projectの扱い

標準のTodo / In Progress / Doneを使います。フォームのProject指定は、作成者がProject編集権限を持つ場合に機能します。CLI/APIや権限のない作成者によるIssueは手動追加が必要です。専用Tokenを使う自動追加Botは作りません。

ProjectのStatusは進捗表示です。Doneへの変更やIssue closeだけでは、マージ・承認・デプロイは許可されません。組み込みのauto-addや追加ビューは、必要ならProjectの画面で設定できます。

## 本番に向けて別途必要なもの

このデモはSOX適合性や本番の統制有効性を証明しません。組織Team・正式な承認者資格・要求の承認版・ITSM連携・本番直前と再実行時の承認照合・クラウド権限・監査用保管は未実装です。artifactの30日保持はデモ用で、正式な証跡保存期間の代替ではありません。

同じRepositoryのAdminは保護設定自体を変更できます。本番では設定管理権限と実行・承認権限の分離を確認してください。Rollbackは新たな承認付き実行として設計する必要があります。
