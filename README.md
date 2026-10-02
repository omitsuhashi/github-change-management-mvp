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

## 一人で実演する場合の例外案（未適用）

レビュー担当者を別途用意できない場合、この公開サンドボックス内だけで、実演中に以下の例外を使い、完了または失敗時に元へ戻す方式を提案します。設定変更はまだ行っていません。

| 対象 | 実演中の変更 | 維持する条件 |
| --- | --- | --- |
| PR #2 | Repository AdminへPR経由のレビューbypassを一時付与 | CIのtest、mainの直接push・force push・削除禁止はbypassなしの別Rulesetで維持 |
| production-demo | 自己承認防止を一時的にオフ | 指定承認者、明示的な承認待ち、許可タグ、管理者による承認bypass禁止を維持 |
| 正式タグ | 変更なし | 既存タグの移動・削除禁止 |

1. 最新PRのSHAとCI成功を確認し、例外の理由・対象をPRに記録します。
2. CIと履歴保護をbypassのない別Rulesetへ分離してから、PRだけに例外を適用します。
3. 確認したHEADのPR #2を例外マージし、新しいv1.0.1タグでstaging検証します。
4. production-demoの承認待ちで所有者が対象版を承認し、同じ成果物の模擬反映と保存された結果を確認します。
5. レビューbypassと自己承認の許可を元に戻し、結果をIssueとProjectへ反映します。途中失敗でも保護設定を復旧します。

この方式は一人で実演するための限定例外です。別人による独立したレビュー・承認の実証にはなりません。例外は実演中だけ有効とし、本番や別リポジトリへは適用しません。実演後に繰り返す場合も同じ例外・復旧手順が必要です。

[PR-only bypass](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository) / [Environmentの承認](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)

## Projectの扱い

標準のTodo / In Progress / Doneを使います。フォームのProject指定は、作成者がProject編集権限を持つ場合に機能します。CLI/APIや権限のない作成者によるIssueは手動追加が必要です。専用Tokenを使う自動追加Botは作りません。

ProjectのStatusは進捗表示です。Doneへの変更やIssue closeだけでは、マージ・承認・デプロイは許可されません。組み込みのauto-addや追加ビューは、必要ならProjectの画面で設定できます。

## 本番に向けて別途必要なもの

このデモはSOX適合性や本番の統制有効性を証明しません。組織Team・正式な承認者資格・要求の承認版・ITSM連携・本番直前と再実行時の承認照合・クラウド権限・監査用保管は未実装です。artifactの30日保持はデモ用で、正式な証跡保存期間の代替ではありません。

同じRepositoryのAdminは保護設定自体を変更できます。本番では設定管理権限と実行・承認権限の分離を確認してください。Rollbackは新たな承認付き実行として設計する必要があります。
