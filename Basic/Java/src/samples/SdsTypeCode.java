<# SdsTypeCode.java

   Copyright (C) 2018 OSIsoft, LLC. All rights reserved.

   THIS SOFTWARE CONTAINS CONFIDENTIAL INFORMATION AND TRADE SECRETS OF
   OSIsoft, LLC.  USE, DISCLOSURE, OR REPRODUCTION IS PROHIBITED WITHOUT
   THE PRIOR EXPRESS WRITTEN PERMISSION OF OSIsoft, LLC.

   RESTRICTED RIGHTS LEGEND
   Use, duplication, or disclosure by the Government is subject to restrictions
   as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and
   Computer Software clause at DFARS 252.227.7013

   OSIsoft, LLC
   1600 Alvarado St, San Leandro, CA 94577
#>

package samples;

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
    BigDecimal(16),
    Calendar(17),
    String(18),
    DateTimeOffset(20),
    Version(22);

    private final int SdsTypeCode;

    SdsTypeCode(int id) {
        this.SdsTypeCode = id;
    }

    public int getValue() {
        return SdsTypeCode;
    }
}
