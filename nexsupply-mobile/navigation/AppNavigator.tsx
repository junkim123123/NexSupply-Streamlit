import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import HomeScreen from "../screens/HomeScreen";
import ResultsScreen from "../screens/ResultsScreen";
import ConsultationScreen from "../screens/ConsultationScreen";

export type RootStackParamList = {
  Home: undefined;
  Results: { result: any };
  Consultation: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Home"
        screenOptions={{
          headerStyle: {
            backgroundColor: "#007AFF",
          },
          headerTintColor: "#fff",
          headerTitleStyle: {
            fontWeight: "bold",
          },
        }}
      >
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: "NexSupply" }}
        />
        <Stack.Screen
          name="Results"
          component={ResultsScreen}
          options={{ title: "분석 결과" }}
        />
        <Stack.Screen
          name="Consultation"
          component={ConsultationScreen}
          options={{ title: "상담 요청" }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}



