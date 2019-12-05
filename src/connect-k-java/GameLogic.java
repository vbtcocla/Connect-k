import java.util.*;
import java.io.*;
import java.lang.*;

public class GameLogic {
	private int col, row, k ,g, f;
	private String mode;
	private boolean debug;
	private ArrayList<AI> aiList;

	public GameLogic(int col, int row, int k, int g,  String mode, int f, boolean debug) {
		this.col = col;
		this.row = row;
		this.k = k;
		this.g = g;
		this.f = f;
		this.mode = mode;
		this.debug = debug;
		aiList = new ArrayList<AI>();
	}

	public void Manual() 
	{
		int player = 1;
		int winPlayer = 0;
		boolean init = true;
		Move move = new Move(-1,-1);
		Board board = new Board(col,row,k,g);
		if (this.f == 1)
		    board.ShowBoard();
		while (true)
		{
			move = aiList.get(player - 1).GetMove(move);
			try
			{
				board = board.MakeMove(move, player);
			}
			catch (InvalidMoveError e)
			{
				winPlayer = player == 1 ? 2 : 1;
				break;
			}

			winPlayer = board.IsWin();
			board.ShowBoard();
			if (winPlayer != 0)
			{
				break;
			}
			player = player == 1 ? 2 : 1;

		}
		if (winPlayer == -1)
		{
		    System.out.println("Tie");
		}
		else
		{
		    System.out.println("Player " + winPlayer + " wins!");
		}

	}

	public void TournamentInterface() 
	{
		Scanner reader = new Scanner(System.in);
		StudentAI ai = new StudentAI(col, row, k, g);
		while (true) 
		{
			int col , row;
			col = reader.nextInt();
			row = reader.nextInt();
			Move result = ai.GetMove(new Move(col, row));
			System.out.println(result.col + " " + result.row + " ");
		}
	}

	public void Run() 
	{
		if ( this.mode.equals("m") )
		{
			AI studentai = new StudentAI(col, row, k, g);
			AI manualai = new ManualAI(col, row, k, g);
			if(this.f == 1) {
			aiList.add(manualai);
			aiList.add(studentai);
			} else {
			aiList.add(studentai);
			aiList.add(manualai);
			}

			Manual();
		}

		else if (mode.equals("t") )
		{
			TournamentInterface();
		}

	}
}