import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
} from "react-native";
import { requestConsultation } from "../services/api";

export default function ConsultationScreen() {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [product, setProduct] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!email.trim()) {
      Alert.alert("오류", "이메일을 입력해주세요.");
      return;
    }

    setLoading(true);

    try {
      const response = await requestConsultation({
        email,
        name,
        product,
        message,
      });

      if (response.success) {
        Alert.alert("성공", "상담 요청이 접수되었습니다.");
        setEmail("");
        setName("");
        setProduct("");
        setMessage("");
      } else {
        Alert.alert("오류", response.error || "요청에 실패했습니다.");
      }
    } catch (error) {
      Alert.alert("오류", "네트워크 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>상담 요청</Text>
        <Text style={styles.subtitle}>전문가와 상담을 원하시면 아래 정보를 입력해주세요.</Text>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>이메일 *</Text>
          <TextInput
            style={styles.input}
            placeholder="your@email.com"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />
        </View>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>이름</Text>
          <TextInput
            style={styles.input}
            placeholder="홍길동"
            value={name}
            onChangeText={setName}
          />
        </View>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>제품/쿼리</Text>
          <TextInput
            style={styles.input}
            placeholder="관심 있는 제품을 입력하세요"
            value={product}
            onChangeText={setProduct}
          />
        </View>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>메시지</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            placeholder="추가 정보나 질문을 입력하세요"
            value={message}
            onChangeText={setMessage}
            multiline
            numberOfLines={4}
          />
        </View>

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleSubmit}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>상담 요청하기</Text>
          )}
        </TouchableOpacity>
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
    marginBottom: 8,
    color: "#333",
  },
  subtitle: {
    fontSize: 14,
    color: "#666",
    marginBottom: 32,
  },
  inputContainer: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: "600",
    marginBottom: 8,
    color: "#333",
  },
  input: {
    borderWidth: 1,
    borderColor: "#ddd",
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: "#f9f9f9",
  },
  textArea: {
    height: 100,
    textAlignVertical: "top",
  },
  button: {
    backgroundColor: "#007AFF",
    borderRadius: 8,
    padding: 16,
    alignItems: "center",
    marginTop: 8,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
});

