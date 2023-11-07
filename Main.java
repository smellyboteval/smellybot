import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);

        int input;
        do {
            System.out.println("Enter number of pieces");
            while (!scanner.hasNextInt()) { // validating element choosing
                System.out.println("Invalid input");
                scanner.next();
            }
             input=scanner.nextInt();
        }while (input<=0);

         // validating strategy choice
        int strategy;
        do {
            System.out.println("1 - Perfect Strategy\n2 - Random Strategy");
            while (!scanner.hasNextInt()) {
                System.out.println("Invalid input");
                scanner.next();
            }
            strategy=scanner.nextInt();
        }while (strategy<=0 || strategy>2);

        System.out.println("Do you want to go first (true/false) ");
        boolean turn;
            while (!scanner.hasNextBoolean()) { // validating turn choice
                System.out.println("Invalid input");
                scanner.next();
            }
            turn=scanner.nextBoolean();
        GameTree gameTree=new GameTree(input);
        gameTree.root.level=turn;
        gameTree.generateGameTree();
        gameTree.assignMinMaxValues();
        if(strategy==1)
            gameTree.playPerfectly();
        if (strategy==2)
            gameTree.playRandomly();





    }
}
