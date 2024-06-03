package dev.jezzy.swimmyfish;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.TextureRegion;
import com.badlogic.gdx.scenes.scene2d.Group;
import com.badlogic.gdx.scenes.scene2d.ui.Label;
import com.badlogic.gdx.utils.Align;

public class GameOver extends Group {
    private final SwimmyFish game;
    private final TextureRegion skeleton;
    private final BitmapFont font;
    private final Label text1;
    private final Label text2;

    public GameOver(SwimmyFish game) {
        this.game = game;
        skeleton = game.atlas.findRegion("dead fish");
        font = new BitmapFont(Gdx.files.internal("font.fnt"));
        Label.LabelStyle labelStyle = new Label.LabelStyle(font, null);
        text1 = new Label("Oops!", labelStyle);
        text2 = new Label("Press enter to try again", labelStyle);
        addActor(text1);
        addActor(text2);
    }

    @Override
    public void draw(Batch batch, float parentAlpha) {
        batch.draw(skeleton, game.camera.position.x - skeleton.getRegionWidth() / 2f,
                   game.viewport.getWorldHeight() - skeleton.getRegionHeight() * 2f);
        text1.setPosition(game.camera.position.x, game.camera.viewportHeight / 3, Align.center);
        text2.setPosition(game.camera.position.x,
                          (game.camera.viewportHeight / 3) - text1.getHeight(), Align.center);
        text1.draw(batch, parentAlpha);
        text2.draw(batch, parentAlpha);
    }

    public void dispose() {
        font.dispose();
    }
}
