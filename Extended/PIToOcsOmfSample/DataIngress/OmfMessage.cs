using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;

namespace PIToOcsOmfSample.DataIngress
{
    /// <summary>
    /// Contains a set of properties that map to the OMF message header values and a byte 
    /// array to hold the OMF message body. These properties and this message body contain all
    /// the information needed to create an HTTP request containing an OMF message.
    /// This class also supports compressing and decompressing of the OMF message body.
    /// </summary>
    public class OmfMessage
    {
        public const string HeaderKey_ProducerToken = "producertoken";
        public const string HeaderKey_MessageType = "messagetype";
        public const string HeaderKey_MessageFormat = "messageformat";
        public const string HeaderKey_MessageCompression = "compression";
        public const string HeaderKey_Action = "action";
        public const string HeaderKey_Version = "omfversion";

        public OmfMessage()
        {
            Headers = new Dictionary<string, string>();
        }

        public IDictionary<string, string> Headers { get; private set; }

        public byte[] Body { get; set; }

        public string ProducerToken
        {
            get
            {
                Headers.TryGetValue(HeaderKey_ProducerToken, out string token);
                return token;
            }
            set
            {
                Headers[HeaderKey_ProducerToken] = value;
            }
        }

        public MessageType MessageType
        {
            get
            {
                MessageType type = MessageType.Data;
                if (Headers.TryGetValue(HeaderKey_MessageType, out string headerVal))
                {
                    Enum.TryParse(headerVal, true, out type);
                }

                return type;
            }
            set
            {
                Headers[HeaderKey_MessageType] = value.ToString();
            }
        }

        public MessageFormat MessageFormat
        {
            get
            {
                MessageFormat format = MessageFormat.JSON;
                if (Headers.TryGetValue(HeaderKey_MessageFormat, out string headerVal))
                {
                    Enum.TryParse(headerVal, true, out format);
                }

                return format;
            }
            set
            {
                Headers[HeaderKey_MessageFormat] = value.ToString();
            }
        }

        public MessageCompression MessageCompression
        {
            get
            {
                MessageCompression compression = MessageCompression.None;
                if (Headers.TryGetValue(HeaderKey_MessageCompression, out string headerVal))
                {
                    Enum.TryParse(headerVal, true, out compression);
                }

                return compression;
            }
            set
            {
                Headers[HeaderKey_MessageCompression] = value.ToString();
            }
        }

        public MessageAction Action
        {
            get
            {
                MessageAction action = MessageAction.Create;
                if (Headers.TryGetValue(HeaderKey_Action, out string headerVal))
                {
                    Enum.TryParse(headerVal, true, out action);
                }

                return action;
            }
            set
            {
                Headers[HeaderKey_Action] = value.ToString();
            }
        }

        public string Version
        {
            get
            {
                Headers.TryGetValue(HeaderKey_Version, out string version);
                return version;
            }
            set
            {
                Headers[HeaderKey_Version] = value;
            }
        }

        public void Compress(MessageCompression compressionType)
        {
            if (compressionType != MessageCompression.GZip)
            {
                throw new NotImplementedException("Only GZip compression is currently supported.");
            }

            if (this.MessageCompression != MessageCompression.None)
            {
                throw new InvalidOperationException($"The message has already been compressed using {MessageCompression}");
            }

            Body = GZipCompress(Body);
            MessageCompression = compressionType;
        }

        public void Decompress()
        {
            switch (MessageCompression)
            {
                case MessageCompression.None:
                    break;
                case MessageCompression.GZip:
                    Body = GZipDecompress(Body);
                    break;
                default:
                    throw new InvalidOperationException($"{nameof(MessageCompression)} has an unexpected value, {MessageCompression}.");
            }

            MessageCompression = MessageCompression.None;
        }

        private static byte[] GZipCompress(byte[] uncompressed)
        {
            using (var memory = new MemoryStream())
            using (var gzip = new GZipStream(memory, CompressionMode.Compress, true))
            {
                gzip.Write(uncompressed, 0, uncompressed.Length);
                return memory.ToArray();
            }
        }

        private static byte[] GZipDecompress(byte[] compressed)
        {
            using (var memoryStream = new MemoryStream(compressed))
            using (var stream = new GZipStream(memoryStream, CompressionMode.Decompress))
            {
                const int size = 4096;
                byte[] buffer = new byte[size];
                using (var memory = new MemoryStream())
                {
                    int count = 0;
                    do
                    {
                        count = stream.Read(buffer, 0, size);
                        if (count > 0)
                        {
                            memory.Write(buffer, 0, count);
                        }
                    } while (count > 0);

                    return memory.ToArray();
                }
            }
        }
    }

    public enum MessageType
    {
        Data = 0,
        Container,
        Type
    }

    public enum MessageFormat
    {
        JSON = 0
    }

    public enum MessageCompression
    {
        None = 0,
        GZip
    }

    public enum MessageAction
    {
        Create = 0,
        Update,
        Delete
    }
}
