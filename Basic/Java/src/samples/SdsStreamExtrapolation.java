package samples;

public enum SdsStreamExtrapolation {

    All(0),
    None(1),
    Forward(2),
    Backward(3);

    private final int SdsStreamExtrapolation;

    private SdsStreamExtrapolation(int id) {
        this.SdsStreamExtrapolation = id;
    }

    int getValue() {
        return SdsStreamExtrapolation;
    }
}
