package samples;

public enum QiStreamMode {

    Continuous(0),
    StepwiseContinuousLeading(1),
    StepwiseContinuousTrailing(2),
    Discrete(3);
    private final int QiStreamMode;

    private QiStreamMode(int id) {
        this.QiStreamMode = id;
    }

    public int getValue() {
        return QiStreamMode;
    }
}
