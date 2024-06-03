package dev.jezzy.swimmyfish;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.InputMultiplexer;
import com.badlogic.gdx.InputProcessor;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.audio.Sound;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.utils.ScreenUtils;

public class GameScreen implements Screen {
    public final SwimmyFish game;
    private final Sound deathSound;
    public Stage gameStage;
    public Stage menuStage;
    public InputMultiplexer inputMultiplexer;
    public Overlay overlay;
    public InputProcessor startInputProcessor;
    public InputProcessor playingInputProcessor;
    public InputProcessor gameOverInputProcessor;
    public GameOver gameOver;
    public Start start;
    private GameWorld world;
    private boolean paused;

    public GameScreen(final SwimmyFish game) {
        this.game = game;

        deathSound = Gdx.audio.newSound(Gdx.files.internal("death.wav"));

        setState(State.START);
    }

    public void setState(State state) {
        switch (state) {
            case START:
                if (world != null) {
                    world.dispose();
                }
                if (gameOver != null) {
                    gameOver.dispose();
                }
                if (gameStage != null) {
                    gameStage.dispose();
                }
                if (menuStage != null) {
                    menuStage.dispose();
                }

                gameStage = new Stage(this.game.viewport);
                menuStage = new Stage(this.game.viewport);
                inputMultiplexer = new InputMultiplexer();
                world = new GameWorld(game, this);
                inputMultiplexer.addProcessor(startInputProcessor);
                inputMultiplexer.addProcessor(playingInputProcessor);
                inputMultiplexer.addProcessor(gameOverInputProcessor);
                Gdx.input.setInputProcessor(inputMultiplexer);

                gameOver = new GameOver(this.game);
                menuStage.addActor(gameOver);

                start = new Start(game, () -> setState(State.PLAYING));
                menuStage.addActor(start);

                paused = true;
                world = new GameWorld(game, this);
                start.setVisible(true);
                world.score.setVisible(false);
                overlay.setVisible(true);
                gameOver.setVisible(false);
                inputMultiplexer.setProcessors(startInputProcessor);
                break;
            case PLAYING:
                for (int i = 0; i < world.obstacles.size; i++) {
                    ObstacleFishPair obstacle = world.obstacles.get(i);
                    obstacle.getTopFish().setVisible(true);
                    obstacle.getBottomFish().setVisible(true);
                }

                paused = false;
                start.setVisible(false);
                world.score.setVisible(true);
                overlay.setVisible(false);
                gameOver.setVisible(false);
                inputMultiplexer.setProcessors(playingInputProcessor);
                break;
            case GAME_OVER:
                paused = true;
                deathSound.play();
                start.setVisible(false);
                overlay.setVisible(true);
                gameOver.setVisible(true);
                inputMultiplexer.setProcessors(gameOverInputProcessor);
                break;
        }
    }

    public boolean isPaused() {
        return paused;
    }

    @Override
    public void show() {}

    @Override
    public void render(float deltaTime) {
        ScreenUtils.clear(new Color(0xEBF9FCff));

        if (!paused) {
            world.update(deltaTime);
        }

        gameStage.draw();
        menuStage.act();
        menuStage.draw();
    }

    @Override
    public void resize(int ignoredWidth, int ignoredHeight) {
        // do nothing
    }

    @Override
    public void pause() {
        paused = true;
        overlay.setVisible(true);
    }

    @Override
    public void resume() {
        paused = false;
        overlay.setVisible(false);
    }

    @Override
    public void hide() {
        pause();
    }

    @Override
    public void dispose() {
        deathSound.dispose();
        gameStage.dispose();
        menuStage.dispose();
        world.dispose();
        overlay.dispose();
        gameOver.dispose();
    }

    public enum State {
        START, PLAYING, GAME_OVER
    }
}
