import React from "react";
import { View, Text, StyleSheet, ScrollView } from "react-native";

interface ResultsScreenProps {
  route: {
    params: {
      result: any;
    };
  };
}

export default function ResultsScreen({ route }: ResultsScreenProps) {
  const { result } = route.params || {};

  if (!result) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>결과 데이터가 없습니다.</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>분석 결과</Text>
        <View style={styles.resultBox}>
          <Text style={styles.resultText}>{JSON.stringify(result, null, 2)}</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
  content: {
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 16,
    color: "#333",
  },
  resultBox: {
    backgroundColor: "#f5f5f5",
    borderRadius: 8,
    padding: 16,
  },
  resultText: {
    fontSize: 14,
    color: "#666",
    fontFamily: "monospace",
  },
  errorText: {
    fontSize: 16,
    color: "#999",
    textAlign: "center",
    marginTop: 40,
  },
});



