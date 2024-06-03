package dev.jezzy.swimmyfish;

import com.badlogic.gdx.Input;
import com.badlogic.gdx.InputAdapter;
import com.badlogic.gdx.math.Intersector;
import com.badlogic.gdx.utils.Align;
import com.badlogic.gdx.utils.Array;

public class GameWorld {
    public static final int OBSTACLE_SPACING = 300;
    public static final int NUMBER_OF_OBSTACLES = 6;
    private final SwimmyFish game;
    private final GameScreen gameScreen;
    private final Background background;
    private final PlayerFish player;
    public final Score score;
    public final Array<ObstacleFishPair> obstacles;
    private ObstacleFishPair closestObstacle;

    public GameWorld(SwimmyFish game, GameScreen gameScreen) {
        this.game = game;
        this.gameScreen = gameScreen;

        background = new Background(this.game);
        gameScreen.gameStage.addActor(background);

        obstacles = new Array<>();
        float obstacleWidth = new ObstacleFish(game, gameScreen, false, 0, 0, 0).getWidth();
        for (int i = 1; i <= NUMBER_OF_OBSTACLES; i++) {
            ObstacleFishPair obstacle =
                    new ObstacleFishPair(game, gameScreen, (OBSTACLE_SPACING + obstacleWidth) * i);
            obstacle.getBottomFish().setVisible(false);
            obstacle.getTopFish().setVisible(false);
            gameScreen.gameStage.addActor(obstacle.getBottomFish());
            gameScreen.gameStage.addActor(obstacle.getTopFish());
            obstacles.add(obstacle);
        }
        closestObstacle = obstacles.first();

        player = new PlayerFish(this.game);
        player.setX(OBSTACLE_SPACING / -2f);
        player.setY(game.camera.viewportHeight / 2, Align.center);
        gameScreen.gameStage.addActor(player);
        gameScreen.gameStage.setKeyboardFocus(player);

        gameScreen.overlay = new Overlay(game);
        gameScreen.overlay.setVisible(false);
        gameScreen.gameStage.addActor(gameScreen.overlay);

        score = new Score(this.game);
        gameScreen.gameStage.addActor(score);

        gameScreen.startInputProcessor = new InputAdapter() {
            @Override
            public boolean keyDown(int keycode) {
                if (keycode == Input.Keys.ESCAPE) {
                    if (gameScreen.isPaused()) {
                        gameScreen.resume();
                    } else {
                        gameScreen.pause();
                    }
                    return true;
                }
                return false;
            }
        };
        gameScreen.playingInputProcessor = new InputAdapter() {
            @Override
            public boolean keyDown(int keycode) {
                if (keycode == Input.Keys.SPACE) {
                    player.jump();
                    return true;
                } else if (keycode == Input.Keys.ESCAPE) {
                    if (gameScreen.isPaused()) {
                        gameScreen.resume();
                    } else {
                        gameScreen.pause();
                    }
                    return true;
                }
                return false;
            }
        };
        gameScreen.gameOverInputProcessor = new InputAdapter() {
            @Override
            public boolean keyDown(int keycode) {
                if (keycode == Input.Keys.ENTER) {
                    gameScreen.setState(GameScreen.State.START);
                    return true;
                }
                return false;
            }
        };
    }

    public void update(float deltaTime) {
        player.update(deltaTime);
        game.camera.position.x = player.getX() + OBSTACLE_SPACING;
        game.camera.update();

        for (ObstacleFishPair obstacle : new Array.ArrayIterator<>(obstacles)) {
            if (game.camera.position.x - game.camera.viewportWidth / 2 >
                obstacle.getX() + obstacle.getWidth())
            {
                obstacle.update(obstacle.getX() +
                                (obstacle.getWidth() + OBSTACLE_SPACING) * NUMBER_OF_OBSTACLES);
            }
            if (Intersector.overlaps(player.getBounds(), obstacle.getBottomFish().getBounds()) ||
                Intersector.overlaps(player.getBounds(), obstacle.getTopFish().getBounds()))
            {
                gameScreen.setState(GameScreen.State.GAME_OVER);
            }
            if (player.getY() < 0 - player.getHeight()) {
                gameScreen.setState(GameScreen.State.GAME_OVER);
            }
        }

        if (player.getX(Align.center) > closestObstacle.getX() + closestObstacle.getWidth()) {
            if (!closestObstacle.isPassed()) {
                score.update();
                player.increaseSpeed();

                closestObstacle.setPassed(true);
                obstacles.removeValue(closestObstacle, true);
                obstacles.add(closestObstacle);
                closestObstacle = obstacles.first();
                closestObstacle.setPassed(false);
            }
        }
    }

    public void dispose() {
        background.dispose();
        for (ObstacleFishPair obstacle : new Array.ArrayIterator<>(obstacles)) {
            obstacle.dispose();
        }
        player.dispose();
        score.dispose();
    }
}
