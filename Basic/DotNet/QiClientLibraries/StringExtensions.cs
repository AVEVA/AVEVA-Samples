using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Runtime.InteropServices;
using System.Security;

namespace QiClientLibsSample
{
    public static class StringExtensions
    {
        #region Secure string handling.

        /// ------------------------------------------------------------------------------------------------
        /// <summary>Convert a string to a SecureString.</summary>
        /// <exception cref="ArgumentNullException">Thrown when one or more required arguments are null.</exception>
        /// <param name="unsecureString">Unsecure string to convert.</param>
        /// <returns>SecureString returned.</returns>
        /// ------------------------------------------------------------------------------------------------
        public static SecureString ConvertToSecureString(this string unsecureString)
        {
            // Sanity check...
            if (unsecureString == null)
            {
                throw new ArgumentNullException("unsecureString is null");
            }

            // Create a SecureString and copy the contents of the string to the SecureString.
            SecureString secureString = new SecureString();
            foreach (char c in unsecureString)
            {
                secureString.AppendChar(c);
            }

            // Make the SecureString read-only.
            secureString.MakeReadOnly();

            // Return it.
            return secureString;
        }

        #endregion
    }
}
