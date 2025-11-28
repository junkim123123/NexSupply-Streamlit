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
import { useNavigation } from "@react-navigation/native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { RootStackParamList } from "../navigation/AppNavigator";
import { analyze } from "../services/api";

type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export default function HomeScreen() {
  const navigation = useNavigation<NavigationProp>();
  const [productName, setProductName] = useState("");
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!productName.trim() && !query.trim()) {
      Alert.alert("오류", "제품명 또는 쿼리를 입력해주세요.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const response = await analyze({
        product_name: productName,
        query: query,
      });

      if (response.success) {
        setResult(response.data);
        navigation.navigate("Results", { result: response.data });
      } else {
        Alert.alert("오류", response.error || "분석에 실패했습니다.");
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
        <Text style={styles.title}>NexSupply</Text>
        <Text style={styles.subtitle}>B2B 소싱 인텔리전스 플랫폼</Text>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>제품명</Text>
          <TextInput
            style={styles.input}
            placeholder="예: USB 케이블"
            value={productName}
            onChangeText={setProductName}
          />
        </View>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>쿼리</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            placeholder="제품에 대한 추가 정보를 입력하세요"
            value={query}
            onChangeText={setQuery}
            multiline
            numberOfLines={4}
          />
        </View>

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleAnalyze}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>분석하기</Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, styles.buttonSecondary]}
          onPress={() => navigation.navigate("Consultation")}
        >
          <Text style={styles.buttonSecondaryText}>전문가 상담 요청</Text>
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
    fontSize: 32,
    fontWeight: "bold",
    marginBottom: 8,
    color: "#333",
  },
  subtitle: {
    fontSize: 16,
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
  buttonSecondary: {
    backgroundColor: "#34C759",
    marginTop: 12,
  },
  buttonSecondaryText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
});

