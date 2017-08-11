package samples;

public enum QiStreamExtrapolation {

    All(0),
    None(1),
    Forward(2),
    Backward(3);

    private final int QiStreamExtrapolation;

    private QiStreamExtrapolation(int id) {
        this.QiStreamExtrapolation = id;
    }

    int getValue() {
        return QiStreamExtrapolation;
    }
}
