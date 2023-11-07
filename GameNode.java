public class GameNode {
    boolean level;
    int minMaxValue;
    int numberOfPieces;
    GameNode rightChild;
    GameNode leftChild;
    public GameNode(int numberOfPieces) {
       this.numberOfPieces =numberOfPieces;
       minMaxValue = 0; //indeterminate
         level = true;// first player
        rightChild=null;
        leftChild=null;

    }
    public boolean isWinning(){
        return numberOfPieces ==0;
    }
    public boolean isTerminal(){
        return isWinning() ;
    }
    public GameNode takeOne(){
        GameNode tmp;
        if(numberOfPieces==1)
            tmp=new GameNode(0);
        else
            tmp=new GameNode(numberOfPieces-1);
        tmp.level=changeTurn();
        return tmp;
    }
    public GameNode takeTwo(){
        GameNode tmp;
        if(numberOfPieces==1)
            tmp=new GameNode(0);
        else
            tmp=new GameNode(numberOfPieces-2);
        tmp.level=changeTurn();
        return tmp;
    }
    public boolean changeTurn(){
        if(level)
            return false;
        else
            return true;
    }
    public String toString(){
        return numberOfPieces+" ";
    }


}
