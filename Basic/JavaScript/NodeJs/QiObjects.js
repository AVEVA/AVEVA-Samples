
module.exports = {
    // enumerates existing Qi types
    qiTypeCode: {
        Empty: 0,
        "Object": 1,
        DBNull: 2,
        "Boolean": 3,
        Char: 4,
        SByte: 5,
        Byte: 6,
        Int16: 7,
        UInt16: 8,
        Int32: 9,
        UInt32: 10,
        Int64: 11,
        UInt64: 12,
        Single: 13,
        Double: 14,
        Decimal: 15,
        DateTime: 16,
        "String": 18,
        Guid: 19,
        DateTimeOffset: 20,
        TimeSpan: 21,
        Version: 22,

        NullableBoolean: 103,
        NullableChar: 104,
        NullableSByte: 105,
        NullableByte: 106,
        NullableInt16: 107,
        NullableUInt16: 108,
        NullableInt32: 109,
        NullableUInt32: 110,
        NullableInt64: 111,
        NullableUInt64: 112,
        NullableSingle: 113,
        NullableDouble: 114,
        NullableDecimal: 115,
        NullableDateTime: 116,
        NullableGuid: 119,
        NullableDateTimeOffset: 120,
        NullableTimeSpan: 121,

        BooleanArray: 203,
        CharArray: 204,
        SByteArray: 205,
        ByteArray: 206,
        Int16Array: 207,
        UInt16Array: 208,
        Int32Array: 209,
        UInt32Array: 210,
        Int64Array: 211,
        UInt64Array: 212,
        SingleArray: 213,
        DoubleArray: 214,
        DecimalArray: 215,
        DateTimeArray: 216,
        StringArray: 218,
        GuidArray: 219,
        DateTimeOffsetArray: 220,
        TimeSpanArray: 221,
        VersionArray: 222,

        Array: 400,
        IList: 401,
        IDictionary: 402,
        IEnumerable: 403,

        QiType: 501,
        QiTypeProperty: 502,
        QiView: 503,
        QiViewProperty: 504,
        QiViewMap: 505,
        QiViewMapProperty: 506,
        QiStream: 507,
        QiStreamIndex: 508,
        QiTable: 509,
        QiColumn: 510,
        QiValues: 511,
        QiObject: 512,

        SByteEnum: 605,
        ByteEnum: 606,
        Int16Enum: 607,
        UInt16Enum: 608,
        Int32Enum: 609,
        UInt32Enum: 610,
        Int64Enum: 611,
        UInt64Enum: 612,

        NullableSByteEnum: 705,
        NullableByteEnum: 706,
        NullableInt16Enum: 707,
        NullableUInt16Enum: 708,
        NullableInt32Enum: 709,
        NullableUInt32Enum: 710,
        NullableInt64Enum: 711,
        NullableUInt64Enum: 712
    },

    // enumerates boundary types
    qiBoundaryType: {
        Exact: 0,
        Inside: 1,
        Outside: 2,
        ExactOrCalculated: 3
    },

    // enumerates Qi stream modes
    qiStreamMode: {
        Continuous: 0,
        StepwiseContinuousLeading: 1,
        StepwiseContinuousTrailing: 2,
        Discrete: 3,
        Default: 0
    },

    //Qi Type
    QiType: function (qiType) {
        if (qiType.Id) {
            this.Id = qiType.Id
        }
        if (qiType.Name) {
            this.Name = qiType.Name;
        }
        if (qiType.Description) {
            this.Description = qiType.Description;
        }
        if (qiType.QiTypeCode) {
            this.QiTypeCode = qiType.QiTypeCode;
        }
        if (qiType.Properties) {
            this.Properties = qiType.Properties;
        }
    },


    //Qi Type Property
    QiTypeProperty: function (qiTypeProperty) {
        if (qiTypeProperty.Id) {
            this.Id = qiTypeProperty.Id;
        }
        if (qiTypeProperty.Name) {
            this.Name = qiTypeProperty.Name;
        }
        if (qiTypeProperty.Description) {
            this.Description = qiTypeProperty.Description;
        }
        if (qiTypeProperty.QiType) {
            this.QiType = qiTypeProperty.QiType;
        }
        if (qiTypeProperty.IsKey) {
            this.IsKey = qiTypeProperty.IsKey;
        }
    },


    //Qi Stream Object
    QiStream: function (qiStream) {
        this.Id = qiStream.Id;
        this.Name = qiStream.Name;
        this.Description = qiStream.Description;
        this.TypeId = qiStream.TypeId;
        if (qiStream.BehaviorId) {
            this.BehaviorId = qiStream.BehaviorId;
        }
    },

    //Qi Behavior object
    QiBehavior: function (qiBehavor) {
        this.Id = null;
        this.Name = null;
        this.Mode = qiBehavor.Mode;
        this.ExtrapolationMode = null;
        this.Overrides = [];
    }
}