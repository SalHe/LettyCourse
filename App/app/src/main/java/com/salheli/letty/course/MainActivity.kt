package com.salheli.letty.course

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView.settings.apply {
            setSupportZoom(true)
            builtInZoomControls = true
            useWideViewPort = true
        }
        webView.loadUrl("file:///android_asset/h5table/course.html")
    }
}