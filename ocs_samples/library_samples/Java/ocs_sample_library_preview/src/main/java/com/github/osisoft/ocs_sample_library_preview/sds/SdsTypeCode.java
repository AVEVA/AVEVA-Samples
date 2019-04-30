/** SdsTypeCode.java
 * 
 *  Copyright 2019 OSIsoft, LLC
 *  
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *  
 *  http://www.apache.org/licenses/LICENSE-2.0>
 *  
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
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
