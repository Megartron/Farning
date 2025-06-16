import javax.swing.JFrame;

public class Main {
    public static void main(String[] args) {
        // Your code goes here
        System.out.println("Hello, world!");
        JFrame frame = new JFrame("TicTacToe");
        
        TicTacToe game = new TicTacToe(true, frame);
        game.game_loop();
    }
}