package dev.jezzy.swimmyfish;

import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.scenes.scene2d.Actor;
import com.badlogic.gdx.utils.Array;

public class Background extends Actor {
    private final SwimmyFish game;
    private final int tileSize;
    private final Array<Sprite> sandTiles;
    private final Sprite oceanTile;
    private final Sprite waveTile;
    private final Sprite skyTile;

    public Background(SwimmyFish game) {
        this.game = game;
        tileSize = 100;
        sandTiles = game.atlas.createSprites("sand");
        oceanTile = game.atlas.createSprite("ocean");
        waveTile = game.atlas.createSprite("wave");
        skyTile = game.atlas.createSprite("sky");
    }

    public void dispose() {}

    @Override
    public void draw(Batch batch, float parentAlpha) {
        float x = game.camera.position.x - game.camera.viewportWidth / 2;

        for (int j = 0; j < 6; j++) {
            for (int i = 0; i < 10; i++) {
                oceanTile.setBounds(x + tileSize * i, tileSize * (j + 1), tileSize, tileSize);
                oceanTile.draw(batch);
            }
        }

        Array<Sprite> orderedSandTiles = new Array<>();
        orderedSandTiles.add(sandTiles.get(9));
        orderedSandTiles.add(sandTiles.get(6));
        orderedSandTiles.add(sandTiles.get(2));
        orderedSandTiles.add(sandTiles.get(8));
        orderedSandTiles.add(sandTiles.get(7));
        orderedSandTiles.add(sandTiles.get(6));
        orderedSandTiles.add(sandTiles.get(7));
        orderedSandTiles.add(sandTiles.get(8));
        orderedSandTiles.add(sandTiles.get(9));
        orderedSandTiles.add(sandTiles.get(2));
        for (int i = 0; i < 10; i++) {
            oceanTile.setBounds(x + tileSize * i, 0, tileSize, tileSize);
            oceanTile.draw(batch);
            Sprite sandTile = orderedSandTiles.get(i);
            sandTile.setBounds(x + tileSize * i, 0, tileSize, tileSize);
            sandTile.draw(batch);
        }

        for (int i = 0; i < 10; i++) {
            skyTile.setBounds(x + tileSize * i, game.camera.viewportHeight - tileSize, tileSize,
                              tileSize);
            skyTile.draw(batch);
            waveTile.setBounds(x + tileSize * i, game.camera.viewportHeight - tileSize * 1.5f,
                               tileSize, tileSize);
            waveTile.draw(batch);
        }
    }
}
