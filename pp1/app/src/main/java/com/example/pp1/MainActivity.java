package com.example.pp1;

import android.content.Intent;
import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import com.google.android.material.textfield.TextInputEditText;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import android.app.DatePickerDialog;


public class MainActivity extends AppCompatActivity {

    private Calendar lastPeriodDate;
    private TextInputEditText cycleLengthInput;
    private TextView resultText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize UI components
        Button chatBotButton = findViewById(R.id.chatBotButton);
        Button datePickerButton = findViewById(R.id.datePickerButton);
        Button calculateButton = findViewById(R.id.calculateButton);
        cycleLengthInput = findViewById(R.id.cycleLengthInput);
        resultText = findViewById(R.id.resultText);

        // Navigate to ChatBotActivity
        chatBotButton.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, ChatBotActivity.class);
            startActivity(intent);
        });

        // Date picker logic
        datePickerButton.setOnClickListener(v -> showDatePicker());

        // Calculate phase logic
        calculateButton.setOnClickListener(v -> {
            if (lastPeriodDate != null) {
                calculatePhase();
            } else {
                resultText.setText("Please select the last period date.");
            }
        });
    }

    private void showDatePicker() {
        final Calendar calendar = Calendar.getInstance();
        int year = calendar.get(Calendar.YEAR);
        int month = calendar.get(Calendar.MONTH);
        int day = calendar.get(Calendar.DAY_OF_MONTH);

        DatePickerDialog datePickerDialog = new DatePickerDialog(this, (view, selectedYear, selectedMonth, selectedDay) -> {
            lastPeriodDate = Calendar.getInstance();
            lastPeriodDate.set(selectedYear, selectedMonth, selectedDay);
            resultText.setText("Selected Date: " + new SimpleDateFormat("yyyy-MM-dd").format(lastPeriodDate.getTime()));
        }, year, month, day);
        datePickerDialog.show();
    }

    private void calculatePhase() {
        int cycleLength = 28; // default cycle length
        String cycleInput = cycleLengthInput.getText().toString();
        if (!cycleInput.isEmpty()) {
            cycleLength = Integer.parseInt(cycleInput);
        }

        Calendar currentDate = Calendar.getInstance();
        long daysPassed = (currentDate.getTimeInMillis() - lastPeriodDate.getTimeInMillis()) / (1000 * 60 * 60 * 24);
        int currentCycleDay = (int) (daysPassed % cycleLength) + 1;

        String currentPhase;
        int daysLeftInPhase;

        if (currentCycleDay >= 1 && currentCycleDay <= 5) {
            currentPhase = "Menstrual Phase";
            daysLeftInPhase = 5 - currentCycleDay;
        } else if (currentCycleDay >= 6 && currentCycleDay <= 13) {
            currentPhase = "Follicular Phase";
            daysLeftInPhase = 13 - currentCycleDay;
        } else if (currentCycleDay == 14) {
            currentPhase = "Ovulation Phase";
            daysLeftInPhase = 0;
        } else {
            currentPhase = "Luteal Phase";
            daysLeftInPhase = cycleLength - currentCycleDay;
        }

        resultText.setText("Current Phase: " + currentPhase + "\nDays left in this phase: " + daysLeftInPhase);
    }
}
