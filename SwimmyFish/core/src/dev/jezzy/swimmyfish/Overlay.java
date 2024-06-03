package dev.jezzy.swimmyfish;

import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.scenes.scene2d.Actor;

public class Overlay extends Actor {
    private final SwimmyFish game;
    private final Sprite sprite;

    public Overlay(SwimmyFish game) {
        this.game = game;
        sprite = game.atlas.createSprite("white overlay");
        sprite.setY(0);
    }

    public void dispose() {}

    @Override
    public void draw(Batch batch, float ignoredParentAlpha) {
        sprite.setX(game.camera.position.x - game.camera.viewportWidth / 2);
        sprite.draw(batch, 0.3f);
    }
}
