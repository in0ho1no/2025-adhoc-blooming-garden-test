"""2048風ゲーム自動プレイスクリプト

このスクリプトはPlaywrightを使用して、2048風のゲームを自動でプレイします。
シンプルな戦略で最短で2048を目指します。
"""

import asyncio
import re
from playwright.async_api import async_playwright, Page


class Game2048AutoPlayer:
    """2048風ゲームの自動プレイヤークラス"""

    def __init__(self, url: str) -> None:
        """初期化

        Args:
            url: ゲームのURL
        """
        self.url = url
        self.move_count = 0
        self.max_tile = 0

    async def get_game_state(self, page: Page) -> dict[str, int | bool]:
        """ゲームの状態を取得

        Args:
            page: Playwrightのページオブジェクト

        Returns:
            ゲーム状態の辞書（スコア、最大タイル値、ゲームオーバーフラグ）
        """
        # スコアを取得
        score_element = await page.query_selector('.score')
        if score_element:
            score_text = await score_element.inner_text()
            score_match = re.search(r'\d+', score_text)
            score = int(score_match.group()) if score_match else 0
        else:
            score = 0

        # グリッド上の最大タイルを取得
        tiles = await page.query_selector_all('.grid-cell')
        max_tile = 0
        for tile in tiles:
            text = await tile.inner_text()
            if text:
                try:
                    value = int(text)
                    max_tile = max(max_tile, value)
                except ValueError:
                    pass

        # ゲームオーバーかどうかを確認
        game_over_element = await page.query_selector('.game-over-overlay')
        is_game_over = False
        if game_over_element:
            style = await game_over_element.get_attribute('style')
            is_game_over = 'display: flex' in (style or '')

        return {'score': score, 'max_tile': max_tile, 'game_over': is_game_over}

    def select_next_move(self, move_count: int) -> str:
        """次の移動方向を選択（シンプルな戦略）

        戦略:
        1. 左下に大きなタイルを集める
        2. 左→下を繰り返し、時々上を使用
        3. 右は最終手段として使用

        Args:
            move_count: 現在の移動回数

        Returns:
            次の移動方向（'a', 's', 'd', 'w'）
        """
        # 基本パターン: 左→下を繰り返す
        pattern = ['a', 's', 'a', 's', 'a', 's', 's']

        # 10手に1回は上を使う
        if move_count % 10 == 9:
            return 'w'

        # 30手に1回は右を使う（行き詰まり回避）
        if move_count % 30 == 29:
            return 'd'

        # 基本パターンをループ
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

            while True:
                # ゲーム状態を取得
                state = await self.get_game_state(page)

                # 最大タイルの更新を記録
                if state['max_tile'] > self.max_tile:
                    self.max_tile = state['max_tile']
                    print(f'🌸 新しいタイルに到達: {self.max_tile} (スコア: {state["score"]})')

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

                # 次の移動を選択
                move = self.select_next_move(self.move_count)
                await page.keyboard.press(move)
                self.move_count += 1

                # 100手ごとに進捗を表示
                if self.move_count % 100 == 0:
                    print(f'📈 進捗: {self.move_count}手目 (最大タイル: {self.max_tile}, スコア: {state["score"]})')

                # 少し待機（アニメーション完了を待つ）
                await asyncio.sleep(0.15)

            print('\n✅ 自動プレイを終了しました')

            # 結果を確認するために少し待機
            await asyncio.sleep(3)
            await browser.close()


async def main() -> None:
    """メイン関数"""
    url = 'https://in0ho1no.github.io/2025-adhoc-blooming-garden/'

    print('🌱 Blooming Garden 自動プレイヤー 🌸')
    print('=' * 50)
    print(f'URL: {url}')
    print('戦略: 左下に大きなタイルを集める')
    print('=' * 50)
    print()

    player = Game2048AutoPlayer(url)
    await player.play_game(headless=False)  # ブラウザを表示してプレイ


if __name__ == '__main__':
    asyncio.run(main())
