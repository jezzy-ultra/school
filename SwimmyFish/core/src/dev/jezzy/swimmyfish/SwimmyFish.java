package dev.jezzy.swimmyfish;

import com.badlogic.gdx.Game;
import com.badlogic.gdx.graphics.Camera;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.g2d.TextureAtlas;
import com.badlogic.gdx.utils.viewport.FitViewport;
import com.badlogic.gdx.utils.viewport.Viewport;

public class SwimmyFish extends Game {
    public final static int WORLD_WIDTH = 1000;
    public final static int WORLD_HEIGHT = 800;
    public TextureAtlas atlas;
    public Camera camera;
    public Viewport viewport;
    public GameScreen gameScreen;

    @Override
    public void create() {
        atlas = new TextureAtlas("pack.atlas");
        camera = new OrthographicCamera();
        viewport = new FitViewport(WORLD_WIDTH, WORLD_HEIGHT, camera);
        gameScreen = new GameScreen(this);

        this.setScreen(gameScreen);
    }

    @Override
    public void dispose() {
        atlas.dispose();
        gameScreen.dispose();
    }

    @Override
    public void render() {
        super.render();
    }
}
