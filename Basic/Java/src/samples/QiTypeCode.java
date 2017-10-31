package samples;

public enum QiTypeCode {
    Empty(0),
    Object(2),
    DBNull(3),
    Boolean(4),
    Char(5),
    Byte(7),
    Int16(8),
    Int32(10),
    Int64(12),
    Float(13),
    Double(14),
    BigDecimal(16),
    Calendar(17),
    String(18),
    DateTimeOffset(20),
    Version(22);

    private final int QiTypeCode;

    QiTypeCode(int id) {
        this.QiTypeCode = id;
    }

    public int getValue() {
        return QiTypeCode;
    }
}
