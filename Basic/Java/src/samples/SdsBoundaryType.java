package samples;

public enum SdsBoundaryType {

    Exact(0),
    Inside(1),
    Outside(2),
    ExactOrCalculated(3);

    private final int SdsBoundaryType;

    private SdsBoundaryType(int id) {
        this.SdsBoundaryType = id;
    }

    public int getValue() {
        return SdsBoundaryType;
    }
}
