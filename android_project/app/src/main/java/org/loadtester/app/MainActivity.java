
package org.loadtester.app;

import android.os.Bundle;
import android.widget.TextView;
import android.widget.Button;
import android.widget.EditText;
import androidx.appcompat.app.AppCompatActivity;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class MainActivity extends AppCompatActivity {
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
        
        TextView output = findViewById(R.id.output);
        Button startBtn = findViewById(R.id.startBtn);
        EditText urlInput = findViewById(R.id.urlInput);
        
        startBtn.setOnClickListener(v -> {
            String url = urlInput.getText().toString();
            output.setText("Starting test for: " + url);
            
            // Run Python script
            Python py = Python.getInstance();
            py.getModule("main");
        });
    }
}
