/** SdsTypeCode.java
 * 
 */

package  com.github.osisoft.ocs_sample_library_preview.sds;

/** 
 * SdsTypeCode 0-22 not inclusive
 */
public enum SdsTypeCode {
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
    Decimal(16),
    DateTime(16),
    Calendar(17),
    String(18),
    DateTimeOffset(20),
    Version(22);

    private final int SdsTypeCode;

    SdsTypeCode(int id) {
        this.SdsTypeCode = id;
    }

    /**
     * gets integer Value
     * @return
     */
    public int getValue() {
        return SdsTypeCode;
    }
}
