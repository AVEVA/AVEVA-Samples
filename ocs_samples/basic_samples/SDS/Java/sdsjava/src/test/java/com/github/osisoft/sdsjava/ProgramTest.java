/** Program.java
 * 
 */
package com.github.osisoft.sdsjava;


import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;


import org.junit.jupiter.api.Test;

/**
 * Test for simple App.
 */
public class ProgramTest
{
    @Test
    public void runMainProgram()
    {
        assertTrue( Program.toRun() );
    }    
}