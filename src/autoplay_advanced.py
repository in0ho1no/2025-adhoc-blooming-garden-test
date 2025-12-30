"""2048風ゲーム自動プレイスクリプト（高度な戦略版）

グリッドの状態を読み取り、より賢い戦略で2048を目指します。
"""

import asyncio
import re
from playwright.async_api import async_playwright, Page


class AdvancedGame2048AutoPlayer:
    """高度な戦略を持つ2048風ゲームの自動プレイヤークラス"""

    def __init__(self, url: str) -> None:
        """初期化

        Args:
            url: ゲームのURL
        """
        self.url = url
        self.move_count = 0
        self.max_tile = 0
        self.stuck_counter = 0

    async def get_grid_state(self, page: Page) -> list[list[int]]:
        """グリッドの状態を取得

        Args:
            page: Playwrightのページオブジェクト

        Returns:
            4x4のグリッド（各セルの値）
        """
        grid = [[0 for _ in range(4)] for _ in range(4)]

        # グリッドセルを取得
        tiles = await page.query_selector_all('.grid-cell')

        for tile in tiles:
            # データ属性から位置を取得
            row_attr = await tile.get_attribute('data-row')
            col_attr = await tile.get_attribute('data-col')

            if row_attr and col_attr:
                row = int(row_attr)
                col = int(col_attr)

                # 値を取得
                text = await tile.inner_text()
                if text:
                    try:
                        value = int(text)
                        grid[row][col] = value
                    except ValueError:
                        pass

        return grid

    async def get_game_state(self, page: Page) -> dict[str, int | bool]:
        """ゲームの状態を取得

        Args:
            page: Playwrightのページオブジェクト

        Returns:
            ゲーム状態の辞書
        """
        # スコアを取得
        score_element = await page.query_selector('.score')
        if score_element:
            score_text = await score_element.inner_text()
            score_match = re.search(r'\d+', score_text)
            score = int(score_match.group()) if score_match else 0
        else:
            score = 0

        # グリッドから最大タイルを取得
        grid = await self.get_grid_state(page)
        max_tile = max(max(row) for row in grid)

        # ゲームオーバーかどうかを確認
        game_over_element = await page.query_selector('.game-over-overlay')
        is_game_over = False
        if game_over_element:
            style = await game_over_element.get_attribute('style')
            is_game_over = 'display: flex' in (style or '')

        return {'score': score, 'max_tile': max_tile, 'game_over': is_game_over, 'grid': grid}

    def find_max_tile_position(self, grid: list[list[int]]) -> tuple[int, int]:
        """最大タイルの位置を取得

        Args:
            grid: 4x4のグリッド

        Returns:
            (row, col)のタプル
        """
        max_val = 0
        max_pos = (0, 0)

        for i in range(4):
            for j in range(4):
                if grid[i][j] > max_val:
                    max_val = grid[i][j]
                    max_pos = (i, j)

        return max_pos

    def select_next_move(self, grid: list[list[int]], move_count: int) -> str:
        """次の移動方向を選択（高度な戦略）

        戦略:
        1. 最大タイルを左下隅（row=3, col=0）に維持
        2. 2番目に大きいタイルを最大タイルの隣に配置
        3. 降順に並べることを目指す

        Args:
            grid: 4x4のグリッド
            move_count: 現在の移動回数

        Returns:
            次の移動方向（'a', 's', 'd', 'w'）
        """
        max_pos = self.find_max_tile_position(grid)
        target_row, target_col = 3, 0  # 左下隅

        # 最大タイルを左下に移動させる
        if max_pos[0] < target_row:
            # 下に移動が必要
            return 's'
        elif max_pos[1] > target_col:
            # 左に移動が必要
            return 'a'

        # 最大タイルが左下にある場合の基本戦略
        # 左→下を中心に、時々他の方向を使用

        # スネーク戦略: 左下から始まって右上に向かう順序
        pattern = ['a', 's', 's', 'a', 's', 'a', 'a', 's']

        # 20手に1回は上を使う（行き詰まり回避）
        if move_count % 20 == 19:
            return 'w'

        # 50手に1回は右を使う（強制的な変化）
        if move_count % 50 == 49:
            return 'd'

        # 行き詰まりカウンターが高い場合はランダムに近い動き
        if self.stuck_counter > 10:
            moves = ['w', 'd', 'a', 's']
            return moves[move_count % 4]

        # 基本パターン
        return pattern[move_count % len(pattern)]

    async def play_game(self, headless: bool = False) -> None:
        """ゲームを自動プレイ

        Args:
            headless: ヘッドレスモードで実行するか
        """
        async with async_playwright() as p:
            # ブラウザを起動
            browser = await p.chromium.launch(headless=headless)
            page = await browser.new_page()

            print(f'🎮 ゲームを開始します: {self.url}')
            await page.goto(self.url)
            await asyncio.sleep(2)  # ページ読み込み待機

            # ゲーム開始
            print('🌱 ゲームスタート！')
            self.move_count = 0
            self.max_tile = 0
            previous_max = 0
            stuck_moves = 0

            while True:
                # ゲーム状態を取得
                state = await self.get_game_state(page)
                grid = state['grid']

                # 最大タイルの更新を記録
                if state['max_tile'] > self.max_tile:
                    self.max_tile = state['max_tile']
                    print(f'🌸 新しいタイルに到達: {self.max_tile} (スコア: {state["score"]}, 移動回数: {self.move_count})')
                    self.stuck_counter = 0  # リセット
                    stuck_moves = 0

                # 進捗がない場合のカウント
                if state['max_tile'] == previous_max:
                    stuck_moves += 1
                    if stuck_moves > 100:
                        self.stuck_counter += 1
                        stuck_moves = 0
                        print(f'⚠️  行き詰まり検出: {self.stuck_counter} (戦略を変更中...)')
                else:
                    stuck_moves = 0

                previous_max = state['max_tile']

                # 2048到達チェック
                if state['max_tile'] >= 2048:
                    print(f'🎊 おめでとうございます！2048に到達しました！')
                    print(f'📊 最終スコア: {state["score"]}')
                    print(f'🎯 移動回数: {self.move_count}')
                    break

                # ゲームオーバーチェック
                if state['game_over']:
                    print(f'💀 ゲームオーバー')
                    print(f'📊 最終スコア: {state["score"]}')
                    print(f'🌺 到達した最大タイル: {self.max_tile}')
                    print(f'🎯 移動回数: {self.move_count}')
                    break

                # 500手でタイムアウト（無限ループ防止）
                if self.move_count > 500:
                    print(f'⏱️  タイムアウト: 500手を超えました')
                    break

                # 次の移動を選択
                move = self.select_next_move(grid, self.move_count)
                await page.keyboard.press(move)
                self.move_count += 1

                # 50手ごとに進捗を表示
                if self.move_count % 50 == 0:
                    print(f'📈 進捗: {self.move_count}手目 (最大タイル: {self.max_tile}, スコア: {state["score"]})')

                # 少し待機（アニメーション完了を待つ）
                await asyncio.sleep(0.15)

            print('
✅ 自動プレイを終了しました')

            # 結果を確認するために少し待機
            await asyncio.sleep(3)
            await browser.close()


async def main() -> None:
    """メイン関数"""
    url = 'https://in0ho1no.github.io/2025-adhoc-blooming-garden/'

    print('🌱 Blooming Garden 自動プレイヤー（高度版） 🌸')
    print('=' * 50)
    print(f'URL: {url}')
    print('戦略: グリッド状態を読み取り、最大タイルを左下隅に維持')
    print('=' * 50)
    print()

    player = AdvancedGame2048AutoPlayer(url)
    await player.play_game(headless=False)  # ブラウザを表示してプレイ


if __name__ == '__main__':
    asyncio.run(main())
