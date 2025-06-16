import java.util.Scanner;
import java.util.Timer;

import javax.swing.JButton;
import javax.swing.JFrame;
import java.awt.event.*;
import java.util.Random;

public class TicTacToe{
    String[][] sf = {
        {"#", "#", "#"},
        {"#", "#", "#"},
        {"#", "#", "#"},
    };

    String[][][] alle_Züge = new String[1000][][];

    String gewinner;
    String spieler = "X";
    int gewonnen = -1;
    int runden = 0;
    boolean mensch = true;
    Scanner scan = new Scanner(System.in);
    JFrame frame;
    String id = "";
    JButton clickedButton;
    JButton[][] felder = new JButton[3][3];
    
    public TicTacToe(boolean mensch, JFrame frame){
        this.frame = frame;
        this.mensch = mensch;
        gui_erstellen();
    }

    public boolean gültiger_zug(int row, int column){
        if (!(row < 3 && column < 3)){
            System.out.println("Ungültiger Zug!");
            return false;
        }
        else if (sf[row][column] != "#"){
            System.out.println("Ungültiger Zug!");
            return false;
        }
        return true;
        }
    
    public int gewinnprüfung(String s){
        // Prüfe ob alle in einer Reihe
        int anzahl_figuren_reihe = 0;
        int anzahl_figuren_spalte = 0;
        int leere_felder = 0;
        for (int r = 0; r < 3; r++){
            anzahl_figuren_reihe = 0;
            for (int c = 0; c < 3; c++){
                if (sf[r][c] == "#"){
                    leere_felder++;
                }

                if (sf[r][c] == s){
                    anzahl_figuren_reihe++;
                }

                if (anzahl_figuren_reihe == 3){
                    return 1;
                }
            }
        }

        if (leere_felder == 0){
            return 0;
        }

        for (int c = 0; c < 3; c++){
            anzahl_figuren_spalte = 0;
            for (int r = 0; r < 3; r++){

                if (sf[r][c] == s)
                {
                    anzahl_figuren_spalte++;
                }
                if (anzahl_figuren_spalte == 3)
                {
                    return 1;
                }
            }
        }

        if (sf[1][1] == s){
            if ((sf[0][0] == s && sf[2][2] == s) || (sf[0][2] == s && sf[2][0] == s)){
                return 1;
            }
        }
        return -1;
    }
    
    public int[] computer_move()
    {
        int lenght = 0;
        int[][] mögliche_züge = new int[9][];
        for (int r = 0; r < 3; r++){
            for (int c = 0; c < 3; c++){
                if (sf[r][c] == "#"){
                    mögliche_züge[lenght] = new int[] {r, c};
                    lenght++;
                }
            }
        }

        Random random = new Random();
        int rnd_pos = random.nextInt(lenght);
        int[] rnd_zug = mögliche_züge[rnd_pos];

        return rnd_zug;
    }

    public void sf_anzeigen(){
        System.out.println("Spielfeld:");
        System.out.println("  | 0 | 1 | 2");
        System.out.println("---------------");
        for (int r = 0; r < 3; r++){
            System.out.print(r + " | ");
            for (int c = 0; c < 3; c++)
            {
                    System.out.print(sf[r][c] + " | ");
            }
                System.out.println("");
            System.out.println("---------------");
        }
    }

    public void gui_erstellen() {
        frame.setSize(310, 330);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(null);
        
        ActionListener click = new ActionListener() {
            @Override
            public void actionPerformed(java.awt.event.ActionEvent e) {
                clickedButton = (JButton) e.getSource();
                id = e.getActionCommand();
                System.out.println(id);
            }
        };

        for (int r = 0; r < 3; r++) {
            for (int c = 0; c < 3; c++) {
                felder[r][c] = new JButton();
                felder[r][c].setBounds(r * 100, c * 100, 90, 90);
                felder[r][c].setActionCommand("" + r + "" + c);
                felder[r][c].setText("");
                frame.add(felder[r][c]);
                felder[r][c].addActionListener(click);
            }
        }

        frame.setVisible(true);
    }

    public void sf_gui_update(){
        
    }

    public void game_loop(){
        int column = 0;
        int row = 0;
        boolean erfolg = false;

        while (gewonnen == -1){
            sf_anzeigen();
            if (runden % 2 == 0){
                if (mensch){
                    // Mensch
                    while (!erfolg && mensch){
                        ActionListener a = new ActionListener() {
                            public void actionPerformed(ActionEvent e) {
                                System.out.println("hi");
                            }
                        };
                        new Timer(100, true, a).start();
                        if (id != ""){
                            char[] zug_Array = id.toCharArray();
                            row = zug_Array[0] - '0';
                            column = zug_Array[1] - '0';
                            erfolg = gültiger_zug(row, column);
                        }
                    }
                    erfolg = false;
                    id = "";
                }
                else{
                    // Computer Random
                    int[] comp = computer_move();
                    row = comp[0];
                    column = comp[1];
                }
            }else{
                int[] comp = computer_move();
                row = comp[0];
                column = comp[1];
            }

            // Zug durchführen
            felder[row][column].setText(spieler);
            sf[row][column] = spieler;

            gewonnen = gewinnprüfung(spieler);

            if (spieler == "X"){
                spieler = "O";
            }
            else{
                spieler = "X";
            }
            runden++;
        }
        sf_anzeigen();
        System.out.println("{0} hat gewonnen!");
    }
}
