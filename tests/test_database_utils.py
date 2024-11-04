from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

import unittest
import uuid
import sys
import os
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from entities.db.gamesRepo import repo

NofGames = 10
NofPlayers = NofGames*2

#WRITES TO DB
class test_games_Repo(unittest.TestCase):
    def setUp(self):
        repo.tear_down()
        
    def tearDown(self):
        repo.tear_down()
        assert len(repo.get_games()) == 0

    @patch('entities.db.gamesRepo.Session')
    def test_create_game_db_error(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        # Levantar SQLAlchemyError
        mock_session.commit.side_effect = SQLAlchemyError("Database error")

        gid = str(uuid.uuid4())
        name = "FUNALDELMUNDIAL"
        state = "waiting"
        pid, pid2 = str(uuid.uuid4()), str(uuid.uuid4())

        # Testear SQLAlchemyError levantado (create_game, create_player, add_player_to_game)
        with self.assertRaises(SQLAlchemyError):
            repo.create_game(unique_id=gid, name=name, state=state, creator_id=pid)

        # Ver que se llamó add()
        mock_session.add.assert_called_once()

        # Ver que se llamaron rollback() y close() -- osea que hubo un error
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()
    
    def test_create_get_join(self):
        repo.tear_down()
        player_ids = []
        for _ in range(NofPlayers):
            player_ids.append(str(uuid.uuid4()))
            repo.create_player(name="MESSI",unique_id=player_ids[-1])
        game_ids = []
        for _ in range(NofGames):
            game_ids.append(str(uuid.uuid4()))
            repo.create_game(unique_id=game_ids[-1],name = "FUNALDELMUNDIAL",state="waiting",creator_id=player_ids[_])
        games = repo.get_games()
        for game in games:
            assert game['unique_id'] in game_ids
            assert game['creator'] in player_ids
        assert len(games) == len(game_ids)
        assert repo.get_game(game_id=game_ids[0])['creator'] == player_ids[0]
        #try joining
        repo.add_player_to_game(player_id=player_ids[-1],game_id=game_ids[0])
        assert player_ids[-1] in repo.get_game(game_id=game_ids[0])['players']


    @patch('entities.db.gamesRepo.Session')
    def test_create_player_db_error(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        # Levantar SQLAlchemyError
        mock_session.commit.side_effect = SQLAlchemyError("Database error")

        pid = str(uuid.uuid4())

        # Testear SQLAlchemyError levantado (create_player)
        with self.assertRaises(SQLAlchemyError):
            repo.create_player(name="MESSI",unique_id=pid)

        # Ver que se llamó add()
        mock_session.add.assert_called_once()

        # Ver que se llamaron rollback() y close() -- osea que hubo un error
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()


    @patch('entities.db.gamesRepo.Session')
    def test_get_game_no_result(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        # Levantar NoResultFound
        mock_session.query.return_value.filter_by.return_value.one.side_effect = NoResultFound()

        gid = str(uuid.uuid4())

        # Testear que se levanta ValueError
        with self.assertRaises(ValueError) as context:
            repo.get_game(game_id=gid)

        self.assertEqual(str(context.exception), "Game_model does not exist")

        # Ver que se llama close()
        mock_session.close.assert_called_once()

    @patch('entities.db.gamesRepo.Session')
    def test_get_player_no_result(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        # Levantar NoResultFound
        mock_session.query.return_value.filter_by.return_value.one.side_effect = NoResultFound()

        pid = str(uuid.uuid4())

        # Testear que se levanta ValueError
        with self.assertRaises(ValueError) as context:
            repo.get_player(player_id=pid)

        self.assertEqual(str(context.exception), "Game_model does not exist")

        # Ver que se llama close()
        mock_session.close.assert_called_once()
    
    def test_get_player_figure_cards(self):
        repo.tear_down()
        player_id = str(uuid.uuid4())

        repo.create_player(name="MESSI", unique_id=player_id)
        figure_cards = repo.get_player_figure_cards(player_id=player_id)
        
        assert 'figure_cards' in figure_cards
        assert isinstance(figure_cards['figure_cards'], list)
        for card in figure_cards['figure_cards']:
            assert 'type' in card
            assert 'unique_id' in card
            assert 'state' in card

    @patch('entities.db.gamesRepo.Session')
    def test_get_player_figure_cards_no_result(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        # Levantar NoResultFound
        mock_session.query.return_value.filter_by.return_value.one.side_effect = NoResultFound()

        pid = str(uuid.uuid4())

        with self.assertRaises(ValueError) as context:
            repo.get_player_figure_cards(player_id=pid)

        self.assertEqual(str(context.exception), "Game_model does not exist")

        mock_session.close.assert_called_once()

    @patch('entities.db.gamesRepo.Session')
    def test_add_player_to_game_db_error(self, MockSession):
        gid = str(uuid.uuid4())
        name = "FUNALDELMUNDIAL"
        state = "waiting"
        pid, pid2 = str(uuid.uuid4()), str(uuid.uuid4())

        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_player(name="DIMARIA",unique_id=pid2)
        repo.create_game(unique_id=gid, name=name, state=state, creator_id=pid)

        mock_session = MagicMock()
        MockSession.return_value = mock_session

        # Levantar SQLAlchemyError
        mock_session.commit.side_effect = SQLAlchemyError("Database error")

        # Testear SQLAlchemyError levantado (create_player)
        with self.assertRaises(SQLAlchemyError):
            repo.add_player_to_game(player_id=pid2, game_id=gid)

        # Ver que se llamaron rollback() y close() -- osea que hubo un error
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()

    @patch('entities.db.gamesRepo.Session')
    def test_add_player_to_game_no_result(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        # Levantar NoResultFound
        mock_session.query.return_value.filter_by.return_value.one.side_effect = NoResultFound()

        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())

        # Testear ValueError levantado cuando no encuentra el jugador o juego
        with self.assertRaises(ValueError) as context:
            repo.add_player_to_game(player_id=pid, game_id=gid)

        self.assertEqual(str(context.exception), "Player or Game does not exist")

        # Ver que se llama close()
        mock_session.close.assert_called_once()

    
    def test_create_card(self):
        pid,gid = str(uuid.uuid4()),str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="waiting",creator_id=pid)
        repo.create_card(card_type=2,card_kind='figure',player_id=pid,game_id=gid,state='drawn')
        repo.create_card(card_type=4,card_kind='movement',player_id=pid,game_id=gid)
        player = repo.get_player(pid)
        assert len(player['figure_cards']) == 1
        assert len(player['movement_cards']) == 1
        assert player['movement_cards'][0]['type'] == 4
        assert player['figure_cards'][0]['state'] == 'drawn'
        assert player['figure_cards'][0]['type'] == 2

    def test_remove_player_from_game(self):
        pid, pid2 = str(uuid.uuid4()), str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_player(name="DIMARIA",unique_id=pid2)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="waiting",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        repo.add_player_to_game(player_id=pid2,game_id=gid)
        repo.remove_player_from_game(player_id=pid2, game_id=gid)
        game = repo.get_game(game_id=gid)
        self.assertEqual(len(game['players']), 1)
        self.assertIn(pid, game['players'])

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_remove_non_existent_player_from_game(self, mock_stdout):
        pid, pid2 = str(uuid.uuid4()), str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_player(name="DIMARIA",unique_id=pid2)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="waiting",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        repo.add_player_to_game(player_id=pid2,game_id=gid)
        repo.remove_player_from_game(player_id=pid2, game_id=gid)
        repo.remove_player_from_game(player_id=pid2, game_id=gid) # Borrar a dimaria de nuevo tendria que dar error
        console_output = mock_stdout.getvalue().strip()
        expected_output = f"Player {pid2} is not in game {gid}."
        self.assertIn(expected_output, console_output)

        game = repo.get_game(game_id=gid)
        self.assertEqual(len(game['players']), 1)
        self.assertIn(pid, game['players'])
    
    def test_pass_turn(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        game = repo.get_game(game_id=gid)
        assert game['turn'] == 0
        for _ in range(70):
            repo.pass_turn(game_id = gid)
        game = repo.get_game(game_id=gid)
        assert game['turn'] == 70

    @patch('entities.db.gamesRepo.Session')
    def test_pass_turn_db_error(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        # Levantar SQLAlchemyError
        mock_session.query.return_value.filter_by.return_value.one.return_value = MagicMock(turn=0)

        gid = str(uuid.uuid4())

        # Simular que se levanta SQLAlchemyError al intentar hacer commit
        mock_session.commit.side_effect = SQLAlchemyError("Database error")

        # Testear que se levanta SQLAlchemyError
        with self.assertRaises(SQLAlchemyError):
            repo.pass_turn(game_id=gid)

        # Ver que se llama rollback() y close() -- o sea que hubo un error
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()

    def test_edit_game_state(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="waiting",creator_id=pid)
        repo.edit_game_state(game_id=gid, new_state="started")

        game = repo.get_game(game_id=gid)
        self.assertEqual(game['state'], "started")

    @patch('entities.db.gamesRepo.Session')
    def test_edit_game_state_db_error(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        # Levantar SQLAlchemyError
        mock_session.commit.side_effect = SQLAlchemyError("Database error")

        # Testear SQLAlchemyError levantado
        with self.assertRaises(SQLAlchemyError):
            repo.edit_game_state("game_id", "new_state")

        # Ver que se hayan llamado rollback() y close()
        mock_session.rollback.assert_called_once()
        mock_session.close.assert_called_once()


    def test_take_move_card(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        repo.create_card(card_type=4,card_kind='movement',player_id=None,game_id=gid)
        repo.create_card(card_type=2,card_kind='movement',player_id=None,game_id=gid)
        repo.take_move_card(pid,gid)
        assert len(repo.get_move_deck(gid)) == 1
        assert len(repo.get_player(pid)['movement_cards']) == 1 
    
    def test_drawn_fig_card(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        repo.create_card(card_type=2,card_kind='figure',player_id=pid,game_id=gid,state="not drawn")
        repo.drawn_figure_card(player_id=pid)
        assert repo.get_player(pid)['figure_cards'][0]['state'] == "drawn"

    @patch('entities.db.gamesRepo.Session')
    def test_drawn_figure_card_no_cards(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        pid = str(uuid.uuid4())
        player = MagicMock()
        player.figure_cards = []

        # Simular que se encuentra el jugador pero sin cartas
        mock_session.query.return_value.filter_by.return_value.one_or_none.return_value = player

        captured_output = io.StringIO()
        sys.stdout = captured_output

        repo.drawn_figure_card(player_id=pid)

        # Ver que se imprime el error
        self.assertIn("Error drawing figure card: No figure cards", captured_output.getvalue())

        # Ver que se haya llamado close()
        mock_session.close.assert_called_once()
        
    def test_create_board(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)

        repo.create_board(game_id=gid)
        assert len(repo.get_board(game_id=gid)) == 6 
        for x_coordinate in range(6):
            assert len(repo.get_board(game_id=gid)[x_coordinate]) == 6

    @patch('entities.db.gamesRepo.Session')
    def test_create_board_no_game(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        gid = str(uuid.uuid4())

        # Simular que no se encuentra juego
        mock_session.query.return_value.filter_by.return_value.one_or_none.return_value = None

        captured_output = io.StringIO()
        sys.stdout = captured_output

        repo.create_board(game_id=gid)

        # Ver que se imprime el error
        self.assertIn(f"Error creating board: No game found with ID: {gid}", captured_output.getvalue())

        # Ver que se haya llamado close()
        mock_session.close.assert_called_once()
    
    def test_swap_positions(self):
        pid1 = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid1)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid1)
        repo.add_player_to_game(player_id=pid1,game_id=gid)
        repo.create_board(game_id=gid)
        color1 = repo.get_board(game_id=gid)[0][0]
        color2 = repo.get_board(game_id=gid)[1][0]
        color3 = repo.get_board(game_id=gid)[2][4]
        color4 = repo.get_board(game_id=gid)[2][5]
        repo.swap_positions_board(game_id=gid,x1=0,y1=0,x2=0,y2=1)
        repo.swap_positions_board(game_id=gid,x1=4,y1=2,x2=5,y2=2)
        assert repo.get_board(game_id=gid)[0][0] == color2
        assert repo.get_board(game_id=gid)[1][0] == color1
        assert repo.get_board(game_id=gid)[2][4] == color4
        assert repo.get_board(game_id=gid)[2][5] == color3

    
    @patch('entities.db.gamesRepo.Session')
    def test_swap_positions_board_invalid_coordinates(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        gid = str(uuid.uuid4())

        captured_output = io.StringIO()
        sys.stdout = captured_output

        repo.swap_positions_board(game_id=gid, x1=6, y1=0, x2=0, y2=0)  # Invalid coordinate

        # Ver que se imprime el error
        self.assertIn("Error swapping positions in board: Invalid coordinates", captured_output.getvalue())

        # Ver que se haya llamado close()
        mock_session.close.assert_called_once()

    def test_add_movement(self):
        # set up player with a card 
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        card_id = repo.create_card(card_type=4,card_kind='movement',player_id=None,game_id=gid)['card_id']
        repo.take_move_card(pid,gid)
        
        assert len(repo.get_player_movements(player_id = pid)) == 0

        repo.add_movement(player_id = pid, card_id = card_id, from_x = 0, from_y = 0, to_x = 5, to_y = 5)

        assert len(repo.get_player_movements(player_id = pid)) == 1
        move = repo.get_player_movements(player_id = pid)[0]
        assert move['from_x'] == 0 and move['from_y'] == 0 and move['to_x'] == 5 and move['to_y'] == 5
        card_id = repo.create_card(card_type=4,card_kind='movement',player_id=None,game_id=gid)['card_id']
        repo.take_move_card(pid,gid)

        assert len(repo.get_player_movements(player_id = pid)) == 1

        repo.add_movement(player_id = pid, card_id = card_id, from_x = 1, from_y = 0, to_x = 3, to_y = 3)

        assert len(repo.get_player_movements(player_id = pid)) == 2
        
    def test_remove_movement(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        card_id = repo.create_card(card_type=4,card_kind='movement',player_id=None,game_id=gid)['card_id']
        repo.take_move_card(pid,gid)
        assert len(repo.get_player_movements(player_id = pid)) == 0
        repo.add_movement(player_id=pid,card_id = card_id, from_x = 0, from_y = 0, to_x = 5, to_y = 5)
        assert len(repo.get_player_movements(player_id = pid)) == 1
        repo.remove_top_movement(player_id = pid)
        assert len(repo.get_player_movements(player_id = pid)) == 0
        
    def test_apply_moves(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid) 
        card_id = repo.create_card(card_type=4,card_kind='movement',player_id=None,game_id=gid)['card_id']
        repo.take_move_card(pid,gid)
        repo.add_movement(player_id=pid,card_id = card_id, from_x = 0, from_y = 0, to_x = 5, to_y = 5)
        assert len(repo.get_player_movements(player_id = pid)) == 1
        assert(repo.get_card(card_id)['state'] == 'blocked')
        assert(repo.get_card(card_id)['player_id'] == pid)
        repo.apply_temp_movements(player_id = pid)
        assert len(repo.get_player_movements(player_id = pid)) == 0   
        assert(repo.get_card(card_id)['state'] == 'not drawn')
        assert(repo.get_card(card_id)['player_id'] == None)
        
    @patch('entities.db.gamesRepo.Session')
    def test_get_player_movements_no_result(self, MockSession):
        mock_session = MagicMock()
        MockSession.return_value = mock_session

        player_id = str(uuid.uuid4())
        mock_session.query.return_value.filter_by.return_value.one.side_effect = NoResultFound()

        with self.assertRaises(ValueError) as context:
            repo.get_player_movements(player_id=player_id)

        # Ver que se imprime el error
        self.assertEqual(str(context.exception), "Game_model does not exist")

        # Verificar que se llama a close()
        mock_session.close.assert_called_once()

    def test_discard_card(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        repo.create_card(card_type=2,card_kind='figure',player_id=pid,game_id=gid,state="not drawn")
        repo.drawn_figure_card(player_id=pid)
        assert repo.get_player(pid)['figure_cards'][0]['state'] == "drawn"
        card_id = repo.get_player(player_id = pid)['figure_cards'][0]['unique_id']
        repo.discard_card(card_id = card_id)
        assert repo.get_card(card_id=card_id)['state'] == 'discarded'

    def test_block_card(self):
        pid = str(uuid.uuid4())
        gid = str(uuid.uuid4())
        repo.create_player(name="MESSI",unique_id=pid)
        repo.create_game(unique_id=gid,name = "FUNALDELMUNDIAL",state="started",creator_id=pid)
        repo.add_player_to_game(player_id=pid,game_id=gid)
        repo.create_card(card_type=2,card_kind='figure',player_id=pid,game_id=gid,state="not drawn")
        repo.drawn_figure_card(player_id=pid)
        assert repo.get_player(pid)['figure_cards'][0]['state'] == "drawn"
        card_id = repo.get_player(player_id = pid)['figure_cards'][0]['unique_id']
        repo.block_card(card_id = card_id)
        assert repo.get_card(card_id=card_id)['state'] == 'blocked'

if __name__ == "__main__":
    unittest.main()
    repo.tear_down()