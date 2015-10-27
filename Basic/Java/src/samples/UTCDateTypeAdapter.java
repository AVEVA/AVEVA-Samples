package samples;

import java.lang.reflect.Type;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.Locale;
import java.util.TimeZone;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonParseException;
import com.google.gson.JsonPrimitive;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;
//import com.google.gson.JsonSyntaxException;

class UTCDateTypeAdapter implements JsonSerializer<GregorianCalendar>, JsonDeserializer<GregorianCalendar> 
{
	private final DateFormat dateFormat;

	UTCDateTypeAdapter() {
		dateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.US);
		dateFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
	}


	public synchronized JsonElement serialize(GregorianCalendar calendar, Type type,
			JsonSerializationContext jsonSerializationContext) {
		synchronized (dateFormat)
		{
			String buffer = new String();
			buffer += calendar.get(Calendar.YEAR);
			buffer += "-";
			buffer += twoDigit(calendar.get(Calendar.MONTH) + 1);
			buffer += "-";
			buffer += twoDigit(calendar.get(Calendar.DAY_OF_MONTH));
			buffer += "T";
			buffer += twoDigit(calendar.get(Calendar.HOUR_OF_DAY));
			buffer += ":";
			buffer += twoDigit(calendar.get(Calendar.MINUTE));
			buffer += ":";
			buffer += twoDigit(calendar.get(Calendar.SECOND));
			buffer += ".";
			buffer += twoDigit(calendar.get(Calendar.MILLISECOND) / 10);
			buffer += "Z";
			return new JsonPrimitive(buffer);
		}
	}

	public synchronized GregorianCalendar deserialize(JsonElement jsonElement, Type type,
			JsonDeserializationContext jsonDeserializationContext)
	{
		try
		{
			synchronized (dateFormat)
			{
				Date dt = dateFormat.parse(jsonElement.getAsString());
				GregorianCalendar cal = new GregorianCalendar(TimeZone.getTimeZone("UTC"));
				cal.setTime(dt);
				return cal;
			}
		}
		catch (ParseException e)
		{
			throw new JsonParseException(jsonElement.getAsString(), e);
		}
	}

	private static String twoDigit(int i) {
		if (i >= 0 && i < 10) {
			return "0" + String.valueOf(i);
		}
		return String.valueOf(i);
	}


}

