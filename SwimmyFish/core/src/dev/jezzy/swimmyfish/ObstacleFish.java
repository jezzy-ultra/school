package dev.jezzy.swimmyfish;

import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.math.Rectangle;
import com.badlogic.gdx.scenes.scene2d.Actor;

import java.util.ArrayList;

public class ObstacleFish extends Actor {
    private final GameScreen gameScreen;
    private final boolean isTop;
    private final Sprite headSprite;
    private final ArrayList<Sprite> bodySprites;
    private int bodySegments;

    public ObstacleFish(SwimmyFish game, GameScreen gameScreen, boolean isTop,
                        int totalPossibleBodySegments, int bodySegments, float x)
    {
        this.gameScreen = gameScreen;
        this.isTop = isTop;
        this.bodySegments = bodySegments;

        headSprite = game.atlas.createSprite("obstacle fish head");
        if (isTop) {
            headSprite.setRotation(180);
            headSprite.setFlip(true, false);
        }

        bodySprites = new ArrayList<>();
        for (int i = 0; i < totalPossibleBodySegments; i++) {
            bodySprites.add(game.atlas.createSprite("obstacle fish body"));
        }

        setWidth(game.atlas.findRegion("obstacle fish body").getRegionWidth());
        constructFish(bodySegments, x);
    }

    public void constructFish(int bodySegments, float x) {
        if (isTop) {
            constructTopFish(bodySegments, x);
        } else {
            constructBottomFish(bodySegments, x);
        }
    }

    private void constructTopFish(int bodySegments, float x) {
        this.bodySegments = bodySegments;

        float height = gameScreen.gameStage.getHeight();
        for (int i = 0; i < bodySegments; i++) {
            Sprite sprite = bodySprites.get(i);
            sprite.setX(x);
            sprite.setY(height - sprite.getHeight());
            height -= sprite.getHeight();
        }
        headSprite.setX(x);
        height -= headSprite.getHeight();
        headSprite.setY(height);

        setHeight(height);
        setX(x);
        setY(gameScreen.gameStage.getHeight() - height);
    }

    private void constructBottomFish(int bodySegments, float x) {
        this.bodySegments = bodySegments;

        float height = 0;
        for (int i = 0; i < bodySegments; i++) {
            Sprite sprite = bodySprites.get(i);
            sprite.setX(x);
            sprite.setY(height);
            height += sprite.getHeight();
        }
        headSprite.setX(x);
        headSprite.setY(height);
        height += headSprite.getHeight();

        setHeight(height);
        setX(x);
        setY(0);
    }

    public Rectangle getBounds() {
        Rectangle bounds = headSprite.getBoundingRectangle();
        for (int i = 0; i < bodySegments; i++) {
            bounds = bounds.merge(bodySprites.get(i).getBoundingRectangle());
            bounds.setWidth(bodySprites.get(i).getWidth());
        }
        return bounds;
    }

    public void dispose() {}

    @Override
    public void draw(Batch batch, float ignoredParentAlpha) {
        headSprite.draw(batch);
        for (int i = 0; i < bodySegments; i++) {
            Sprite sprite = bodySprites.get(i);
            sprite.draw(batch);
        }
    }
}
