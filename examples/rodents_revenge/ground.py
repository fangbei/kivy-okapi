import os

# Engine
from okapi.engine.ground import BaseGround

# Local
import actors

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))


class OpenGround(BaseGround):
    project_root = project_root
    sprite_path = 'assets/images/fancy-ground-50.png'

    def can_accommodate(self, actor, delta_x, delta_y, is_pathfinding=False):
        """
        This is the code that pushes rows of blocks!
        If we try to walk onto ground already occupied by an actor,
        we see if that actor is a block. If so, we traverse in the
        direction of the desired movement until we find empty territory,
        at which time we move the entire row of blocks.
        """
        if isinstance(actor, actors.Cat) and self.actor and isinstance(self.actor, actors.Rat):
            if not is_pathfinding:
                self.level.game.lose_life()
            return True

        if isinstance(actor, actors.Rat) and self.actor and isinstance(self.actor, actors.Cheese):
            if not is_pathfinding:
                self.level.game.eat_cheese(self.actor)
            return True

        current_target_x = self.x
        current_target_y = self.y

        movable_row = []
        if self.actor and self.actor.IS_MOVABLE:

            # Only mice can push blocks. Not cats. That would make no
            # real world sense. Come on!
            if not isinstance(actor, actors.Rat):
                return False

            movable_row.append(self.actor)

            while True:
                # Every step through this loop, obviously we must continue
                # to stride out in the desired direction
                current_target_x += delta_x
                current_target_y += delta_y

                # Get ground at the target location
                ground = self.level.get_ground_by_coords(current_target_x, current_target_y)

                # If the ground doesn't exist or is impassible, the whole ruse is up
                if ground is None or not ground.is_passable:
                    return False

                # If the ground has an actor...
                if ground.actor and not getattr(ground.actor, 'IS_SQUISHABLE', False):

                    # Non-blocks are show-stoppers. Ruse is up.
                    if not ground.actor.IS_MOVABLE:
                        return False

                    # Finding more blocks means we push on...
                    else:
                        movable_row.append(ground.actor)

                # Land-ho! We found an empty spot.
                else:

                    actor_is_squishable = getattr(ground.actor, 'IS_SQUISHABLE', False)
                    if actor_is_squishable:
                        ground.actor = None

                    if not is_pathfinding:
                        movable_row.reverse()
                        for actor in movable_row:
                            self.level.game.move_actor(actor, delta_x, delta_y)
                    return True

        return super(OpenGround, self).can_accommodate(actor, delta_x, delta_y)


class CatGround(OpenGround):
    initial_actor_cls = actors.Cat


class HellcatGround(OpenGround):
    initial_actor_cls = actors.Hellcat


class RatGround(OpenGround):
    initial_actor_cls = actors.Rat


class BlockGround(OpenGround):
    initial_actor_cls = actors.Block


class NullGround(OpenGround):
    is_passable = False
    sprite_path = 'assets/images/black.png'


class ImpassableGround(OpenGround):
    is_passable = False
    sprite_path = 'assets/images/fancy-impassable-50.png'
