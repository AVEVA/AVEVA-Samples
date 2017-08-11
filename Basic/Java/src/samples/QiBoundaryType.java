package samples;

public enum QiBoundaryType {

    Exact(0),
    Inside(1),
    Outside(2),
    ExactOrCalculated(3);

    private final int QiBoundaryType;

    private QiBoundaryType(int id) {
        this.QiBoundaryType = id;
    }

    public int getValue() {
        return QiBoundaryType;
    }
}
