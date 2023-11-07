import java.util.Scanner;

public class GameTree {
    GameNode root;
    Scanner scanner = new Scanner(System.in);

    public GameTree(int numberOfPieces) {
        root = new GameNode(numberOfPieces);
    }
    public void generateGameTree(){
        generateGameTree(root);
    }

    private void generateGameTree(GameNode p) {
        if (p.numberOfPieces == 0)
            return;
        else {
            p.rightChild = p.takeTwo();
            p.leftChild = p.takeOne();
            generateGameTree(p.rightChild);
            generateGameTree(p.leftChild);
        }
    }

    public void assignMinMaxValues() {
        assignMinMaxUsingDFS(this.root);
    }

    public int assignMinMaxUsingDFS(GameNode node) {
        if (node == null) {
            return 0;
        }

        if (node.isWinning()) {
            if (!node.level) {
                node.minMaxValue = 1;
                return 1;
            } else {
                node.minMaxValue = -1;
                return -1;
            }
        } else {
            int index = 0;
            int[] minMaxValues = new int[2];

            if (node.rightChild != null)
                minMaxValues[index++] = assignMinMaxUsingDFS(node.rightChild);//0 // to check the childeren null means it's filled
            if (node.leftChild != null)
                minMaxValues[index++] = assignMinMaxUsingDFS(node.leftChild);//-1


            int overAllMin = minMaxValues[0];
            int overAllMax = minMaxValues[0];

            //index must be greater than 0 since all are not terminal nodes

            for (int i = 1; i < index; i++) {
                if (overAllMin > minMaxValues[i]) overAllMin = minMaxValues[i];
                if (overAllMax < minMaxValues[i]) overAllMax = minMaxValues[i];
            }

            if (node.level) {
                node.minMaxValue = overAllMax;
                return overAllMax;
            } else {
                node.minMaxValue = overAllMin;
                return overAllMin;
            }
        }
    }

//    public void breadthFirst() {
//        GameNode p = root;
//        Queue<GameNode> queue = new Queue<>();
//        if (p != null) {
//            queue.enqueue(p);
//            while (!queue.isEmpty()) {
//                p = queue.dequeue();
//                visit(p);
//                if (p.leftChild != null)
//                    queue.enqueue(p.leftChild);
//                if (p.rightChild != null)
//                    queue.enqueue(p.rightChild);
//            }
//        }
//    }

    public void visit(GameNode p) {
        System.out.print(p.numberOfPieces + " " + p.level + " " + "'" + p.minMaxValue + "'" + " ");
    }
    public void playPerfectly(){
        playPerfectly(root);
    }

    private void playPerfectly(GameNode p) {
        if (p.numberOfPieces == 0) { // reach the leaf(End of the program)
            if (p.minMaxValue == -1)
                System.out.println("     # Computer won ☹ #     ");
            if (p.minMaxValue == 1)
                System.out.println("     # You won ☺ #     ");
        } else {
            System.out.println("( "+p.numberOfPieces+" ) "+" Pieces are remaining");
            if (p.level) {// it means my turn
                System.out.println("    ## Your turn ##    ");
                System.out.println("1 : Take One |  2 : Take Two |  3 : Show Hint|  4 : Show Statistics");
                int input = scanner.nextInt();
                if (input == 1)
                    playPerfectly(p.leftChild);
                if (input == 2)
                    playPerfectly(p.rightChild);
                if(input==3) {
                    if (p.leftChild.minMaxValue >= p.rightChild.minMaxValue)
                        System.out.println("Hint : Take one piece");
                    else
                        System.out.println("Hint : Take two pieces");
                    playPerfectly(p);
                }
                if(input==4){
                    System.out.println("Height is "+height()+ " and number of nodes are "+count());
                    playPerfectly(p);
                }

            }
            else { // the computer's turn
                if (p.leftChild.minMaxValue <= p.rightChild.minMaxValue) {
                    System.out.println("    ## Computer took 1 piece ##   ");
                    playPerfectly(p.leftChild);
                }
                else {
                    System.out.println("    ## Computer took 2 pieces ##   ");
                    playPerfectly(p.rightChild);
                }
            }
        }
    }




    public void playRandomly(){
        playRandomly(root);
    }

    private void playRandomly(GameNode p) {
        if (p.numberOfPieces == 0) { // reach the leaf(End of the program)
            if (p.minMaxValue == -1)
                System.out.println("     # Computer won ☹ #     ");
            if (p.minMaxValue == 1)
                System.out.println("     # You won ☺ #     ");
        } else {
            System.out.println("( "+p.numberOfPieces+" ) "+" Pieces are remaining");
            if (p.level) {// it means my turn
                System.out.println("    ## Your turn ##    ");
                System.out.println("1 : Take One |  2 : Take Two |  3 : Show Hint|  4 : Show Statistics");
                int input = scanner.nextInt();
                if (input == 1)
                    playRandomly(p.leftChild);
                if (input == 2)
                    playRandomly(p.rightChild);
                if(input==3) {
                    if (p.leftChild.minMaxValue >= p.rightChild.minMaxValue)
                        System.out.println("Hint : Take one piece");
                    else
                        System.out.println("Hint : Take two pieces");
                    playRandomly(p);
                }
                if(input==4){
                    System.out.println("Height is "+height()+ " and number of nodes are "+count());
                    playRandomly(p);
                }

            }
            else { // the computer's turn
                if ((int)(Math.random()*101)>50) { // 50% will take 1
                    System.out.println("    ## Computer took 1 piece ##   ");
                    playRandomly(p.leftChild);
                }
                else {
                    System.out.println("    ## Computer took 2 pieces ##   ");
                    playRandomly(p.rightChild);
                }
            }
        }
    }







    public int height(){
        if(root==null)
            return 0;
        else if(heightRight(root)>=heightLeft(root))
            return heightRight(root)+1;
        else
            return heightLeft(root)+1;
    }
    private int heightRight(GameNode input){
        if(input==null || isLeaf(input))
            return 0;
        else
            return 1+heightRight(input.rightChild);
    }
    private int heightLeft(GameNode input){
        if(input==null || isLeaf(input))
            return 0;
        else
            return 1+heightLeft(input.leftChild);
    }
    public boolean isLeaf(GameNode p) {
        if(p==null)
            return false;
        else
            return (p.rightChild==null&&p.leftChild==null);
    }
    public int count() {
        return count(root);
    }

    private int count(GameNode input) {
        if (input == null)
            return 0;
        else if(input.numberOfPieces==1)// to handle that if one node has only one piece it count only one child
            return 1+count(input.leftChild);
        else
            return 1 + count(input.rightChild) + count(input.leftChild);
    }
}
