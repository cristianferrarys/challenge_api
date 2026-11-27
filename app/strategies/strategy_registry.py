from app.strategies.notification_strategy import (
    NotificationStrategy,
)

class StrategyRegistry:
    def __init__(
        self,
        strategies: list[NotificationStrategy],
    ):
        self._strategies = {
            strategy.channel: strategy
            for strategy in strategies
        }

    def get_strategy(
        self,
        channel: str,
    ) -> NotificationStrategy:

        strategy = self._strategies.get(
            channel.lower().strip()
        )

        if strategy is None:
            raise ValueError(f"Unsupported channel: {channel}")

        return strategy