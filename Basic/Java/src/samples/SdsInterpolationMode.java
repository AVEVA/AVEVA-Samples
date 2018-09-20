package samples;

public enum SdsInterpolationMode {

    Continuous(0),
    StepwiseContinuousLeading(1),
    StepwiseContinuousTrailing(2),
    Discrete(3);
    private final int SdsInterpolationMode;

    private SdsInterpolationMode(int id) {
        this.SdsInterpolationMode = id;
    }

    public int getValue() {
        return SdsInterpolationMode;
    }
}
