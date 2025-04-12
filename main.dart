import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(CropDiseaseApp());
}

class CropDiseaseApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: DiseaseDetectionScreen(),
    );
  }
}

class DiseaseDetectionScreen extends StatefulWidget {
  @override
  _DiseaseDetectionScreenState createState() => _DiseaseDetectionScreenState();
}

class _DiseaseDetectionScreenState extends State<DiseaseDetectionScreen> {
  File? _image;
  String _result = "";

  Future<void> _pickImage() async {
    final pickedFile = await ImagePicker().pickImage(source: ImageSource.camera);
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path);
      });
    }
  }

  Future<void> _predictDisease() async {
    if (_image == null) return;
    final request = http.MultipartRequest("POST", Uri.parse("http://your-api-url/predict"));
    request.files.add(await http.MultipartFile.fromPath("file", _image!.path));
    final response = await request.send();
    final responseData = await http.Response.fromStream(response);
    final result = jsonDecode(responseData.body);
    setState(() {
      _result = "Class: ${result['class']}, Confidence: ${result['confidence']}";
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Crop Disease Detection")),
      body: Column(
        children: [
          _image == null
              ? Text("No image selected")
              : Image.file(_image!, height: 300),
          ElevatedButton(onPressed: _pickImage, child: Text("Pick Image")),
          ElevatedButton(onPressed: _predictDisease, child: Text("Predict")),
          Text(_result),
        ],
      ),
    );
  }
}
